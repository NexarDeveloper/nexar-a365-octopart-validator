import os
from nexarClient.nexarDesignClient import NexarClient

workspaces_query = """
query workspaces {
    desWorkspaces {
        id
        name
        url
    }
}
"""

projects_query = """
query projects ($workspaceUrl: String!){
    desProjects (
        workspaceUrl: $workspaceUrl
    ){
        nodes {
            id
            name
        }
    }
}
"""

project_releases_query = """
query project_releases ($projectId: ID!){
    desProjectById (
        id: $projectId
    ){
        id
        name
        design {
            releases {
                nodes {
                    id
                    description
                    releaseId
                }
            }
        }
    }
}
"""

release_variants_query = """
query release_variants ($releaseId: ID!) {
    desReleaseById (
        id: $releaseId
    ) {
        id
        variants {
            name
        }
    }
}
"""

client_id = os.environ["NEXAR_CLIENT_ID"]
client_secret = os.environ["NEXAR_CLIENT_SECRET"]
nexar = NexarClient(client_id, client_secret, ["supply.domain", "design.domain", "openid", "user.access"])

def get_workspaces():
    response = nexar.get_query(workspaces_query)
    return response.get("desWorkspaces")

def get_projects(workspace_url):
    response = nexar.get_query(projects_query, {
        "workspaceUrl": workspace_url
    })
    return response.get("desProjects").get("nodes")

def get_project_releases(project_id):
    response = nexar.get_query(project_releases_query, {
        "projectId": project_id
    })
    return response.get("desProjectById").get("design").get("releases").get("nodes")

def get_release_variants(release_id):
    response = nexar.get_query(release_variants_query, {
        "releaseId": release_id
    })
    return response.get("desReleaseById").get("variants")
