import PySimpleGUI as sg
from apiQueries import *

workspace_list_column = [
    [
        sg.Text("Workspaces"),
        sg.Button(
            button_text="Fetch", enable_events=True, key="-FETCH WORKSPACES-"
        )
    ],
    [
        sg.Listbox(
            values = [], enable_events=True, size=(40, 10), key="-WORKSPACES LIST-"
        )
    ]
]

project_list_column = [
    [
        sg.Text("Projects")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 10), key="-PROJECTS LIST-"
        )
    ]
]

release_list_column = [
    [
        sg.Text("Releases")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 10), key="-RELEASES LIST-"
        )
    ]
]

release_variants_list_column = [
    [
        sg.Text("Release Variants")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 10), key="-RELEASE VARIANTS LIST-"
        )
    ]
]

layout = [
    [
        sg.Column(workspace_list_column),
        sg.VSeparator(),
        sg.Column(project_list_column),
        sg.VSeparator(),
        sg.Column(release_list_column),
        sg.VSeparator(),
        sg.Column(release_variants_list_column)
    ],
    [
        # sg.Text("", enable_events=True, key="-BOM-")
        sg.Table(
            values=[],
            headings=["Component", "Description", "MPN", "Manufacturer", "Quantity"],
            auto_size_columns=True,
            justification="center",
            key="-BOM TABLE-",
            enable_events=True,
            expand_x=True
        )
    ],
    [
        sg.Button(
            button_text="Check Octopart for sourcing issues",
            expand_x=True,
            enable_events=True,
            key="-CHECK BUTTON-"
        )
    ]
]

window = sg.Window("A365 BOM Portal", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    elif event == "-FETCH WORKSPACES-":
        window["-WORKSPACES LIST-"].update([])
        window["-PROJECTS LIST-"].update([])
        window["-RELEASES LIST-"].update([])
        window["-RELEASE VARIANTS LIST-"].update([])
        window["-BOM TABLE-"].update([])

        workspaces = get_workspaces()
        workspace_names = []
        for workspace in workspaces:
            workspace_names.append(workspace.get("name"))
        window["-WORKSPACES LIST-"].update(workspace_names)

    elif event == "-WORKSPACES LIST-":
        window["-PROJECTS LIST-"].update([])
        window["-RELEASES LIST-"].update([])
        window["-RELEASE VARIANTS LIST-"].update([])
        window["-BOM TABLE-"].update([])

        for workspace in workspaces:
            if workspace.get("name") == values["-WORKSPACES LIST-"][0]:
                projects = workspace.get("projects")
                break
        
        project_names = []
        for project in projects:
            project_names.append(project.get("name"))
        window["-PROJECTS LIST-"].update(project_names)
    
    elif event == "-PROJECTS LIST-":
        window["-RELEASES LIST-"].update([])
        window["-RELEASE VARIANTS LIST-"].update([])
        window["-BOM TABLE-"].update([])

        for project in projects:
            if project.get("name") == values["-PROJECTS LIST-"][0]:
                project_id = project.get("id")
                break
        
        releases = get_releases(project_id)
        release_names = []
        for release in releases:
            release_names.append(release.get("description"))
        window["-RELEASES LIST-"].update(release_names)
    
    elif event == "-RELEASES LIST-":
        window["-RELEASE VARIANTS LIST-"].update([])
        window["-BOM TABLE-"].update([])

        for release in releases:
            if release.get("description") == values["-RELEASES LIST-"][0]:
                variants = release.get("variants")
                release_id = release.get("id")
                break
        
        variant_names = []
        for variant in variants:
            variant_names.append(variant.get("name"))
        window["-RELEASE VARIANTS LIST-"].update(variant_names)

    elif event == "-RELEASE VARIANTS LIST-":
        window["-BOM TABLE-"].update([])
        variant_name = values["-RELEASE VARIANTS LIST-"][0]
        
        bom = get_bom(release_id, variant_name)
        rows = []
        queries = []
        for bomItem in bom.get("bomItems"):
            component = bomItem.get("component")
            if not component.get("manufacturerParts"):
                continue
            
            mpn = component.get("manufacturerParts")[0].get("partNumber")
            manufacturer = component.get("manufacturerParts")[0].get("companyName")
            queries.append({
                "mpn": mpn,
                "limit": 1,
                "manufacturer": manufacturer,
                "reference": f"{mpn}_{manufacturer}",
            })
            rows.append([
                component.get("name"),
                component.get("description"),
                component.get("manufacturerParts")[0].get("partNumber"),
                component.get("manufacturerParts")[0].get("companyName"),
                bomItem.get("quantity"),
            ])

        window["-BOM TABLE-"].update(rows)
    
    elif event == "-CHECK BUTTON-":
        if not queries:
            continue

        line_items = query_bom(queries)
        for line_item in line_items:
            issues = []
            
            lifecycle = get_spec(line_item.get("parts")[0].get("specs"), "Lifecycle Status")
            
            if lifecycle is None:
                issues.append("Lifecycle status is unknown.")
            elif lifecycle != "Production":
                issues.append(f"Lifecycle status is {lifecycle}")

            totalAvail = line_item.get("parts")[0].get("totalAvail")
            if totalAvail < 1000:
                issues.append(f"Total availability is {totalAvail}")
            
            if not issues:
                continue

            text = f"Issues with query: {line_item.get('reference')} \n\n"
            for issue in issues:
                text += (issue + "\n")
                
            n_of_similar_parts = line_item.get("parts")[0].get("counts").get("similar_parts")
            
            if n_of_similar_parts == 0:
                sg.popup_ok(text, title="Sourcing Issue")
                continue
            
            text += f"\nThere are {n_of_similar_parts} similar parts.\nCheck the similar parts?\n"
            choice = sg.popup_yes_no(text, title="Sourcing Issue")
            
            if choice != "Yes":
                continue
            
            [mpn, manufacturer] = line_item.get("reference").split("_")
            
            similar_parts = get_similar_parts(mpn, manufacturer)

            similar_text = "Similar Parts:\n\n"

            for similar_part in similar_parts:
                similar_text += f"MPN: {similar_part.get('mpn')}\nDescription: {similar_part.get('shortDescription')}\nMedian Price /1000: {similar_part.get('medianPrice1000').get('price')} {similar_part.get('medianPrice1000').get('currency')}\nTotal Availability: {similar_part.get('totalAvail')}\nLifecycle Status: {get_spec(similar_part.get('specs'), 'Lifecycle Status')}\n\n"
            
            sg.popup_scrolled(similar_text, title="Similar Parts", size=(50, 10))


window.close()
