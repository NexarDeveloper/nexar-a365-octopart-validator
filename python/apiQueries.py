import os
from nexarClient.nexarDesignClient import NexarClient

workspace_projects = """
query explorer {
    desWorkspaces {
        id
        name
        url
        projects {
            id
            name
        }
    }
}
"""

release_variants = """
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
                    variants {
                        name
                    }
                }
            }
        }
    }
}
"""

variant_bom = """
query release_variants ($releaseId: ID!, $variantName: String) {
    desReleaseById (
        id: $releaseId
    ) {
        id
        variants (
            where: {
                name: {
                    eq: $variantName
                }
            }
        ){
            name
            bom {
                id
                bomItems {
                    bomItemInstances {
                        designator
                        isFitted
                    }
                    quantity
                    component {
                        id
                        name
                        comment
                        description
                        manufacturerParts {
                            companyName
                            partNumber
                            priority
                            octopartId
                            supplierParts {
                                partNumber
                                companyName
                            }
                        }
                    }
                }
            }
        }
    }
}
"""

client_id = os.environ["NEXAR_CLIENT_ID"]
client_secret = os.environ["NEXAR_CLIENT_SECRET"]
nexar = NexarClient(client_id, client_secret, ["supply.domain", "design.domain", "openid", "user.access"])

def get_workspaces():
    response = nexar.get_query(workspace_projects)
    return response.get("desWorkspaces")

def get_releases(projectId):
    response = nexar.get_query(release_variants, {
        "projectId": projectId
    })
    return response.get("desProjectById").get("design").get("releases").get("nodes")

def get_bom(releaseId, variantName):
    response = nexar.get_query(variant_bom, {
        "releaseId": releaseId,
        "variantName": variantName
    })
    return response.get("desReleaseById").get("variants")[0].get("bom")