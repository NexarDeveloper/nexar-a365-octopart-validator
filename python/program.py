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
    ]
]

window = sg.Window("Nexar Design Portal", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "-FETCH WORKSPACES-":
        workspaces = get_workspaces()
        workspace_names = []
        for workspace in workspaces:
            workspace_names.append(workspace.get("name"))
        window["-WORKSPACES LIST-"].update(workspace_names)

    elif event == "-WORKSPACES LIST-":
        for workspace in workspaces:
            if workspace.get("name") == values["-WORKSPACES LIST-"][0]:
                workspace_url = workspace.get("url")
                break
        
        projects = get_projects(workspace_url)
        project_names = []
        for project in projects:
            project_names.append(project.get("name"))
        window["-PROJECTS LIST-"].update(project_names)
    
    elif event == "-PROJECTS LIST-":
        for project in projects:
            if project.get("name") == values["-PROJECTS LIST-"][0]:
                project_id = project.get("id")
                break
        
        releases = get_project_releases(project_id)
        release_names = []
        for release in releases:
            release_names.append(release.get("description"))
        window["-RELEASES LIST-"].update(release_names)
    
    elif event == "-RELEASES LIST-":
        for release in releases:
            if release.get("description") == values["-RELEASES LIST-"][0]:
                release_id = release.get("id")
                break
        
        variants = get_release_variants(release_id)
        variant_names = []
        for variant in variants:
            variant_names.append(variant.get("name"))
        window["-RELEASE VARIANTS LIST-"].update(variant_names)


window.close()
