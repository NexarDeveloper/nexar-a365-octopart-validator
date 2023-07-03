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
            headings=["Component", "Quantity", "Description"],
            auto_size_columns=True,
            justification="center",
            key="-BOM TABLE-",
            enable_events=True,
            expand_x=True
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
        for bomItem in bom.get("bomItems"):
            component = bomItem.get("component")
            rows.append([
                component.get("name"),
                bomItem.get("quantity"),
                component.get("description")
            ])
        window["-BOM TABLE-"].update(rows)

window.close()
