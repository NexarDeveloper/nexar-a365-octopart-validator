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
                    quantity
                    component {
                        id
                        name
                        comment
                        description
                        manufacturerParts {
                            companyName
                            partNumber
                        }
                    }
                }
            }
        }
    }
}
"""

multi_match = """
query MultiMatchSearch ($queries: [SupPartMatchQuery!]!){
  supMultiMatch(queries: $queries) {
    hits
    reference
    parts {
        id
        name
        mpn
        medianPrice1000 {
            price
            currency
        }
        totalAvail
        estimatedFactoryLeadDays
        counts
        specs {
            attribute {
                name
            }
            value
            units
        }
    }
  }
}
"""

similar_parts = """
query similarParts ($mpn: String!, $manufacturer: String){
    supMultiMatch (
        queries: [
            {
                mpn: $mpn,
                manufacturer: $manufacturer,
                limit: 1
            }
        ]
    ){
        hits
            parts {
                mpn
                similarParts {
                    mpn
                    shortDescription
                    medianPrice1000 {
                        price
                        currency
                    }
                    totalAvail
                    estimatedFactoryLeadDays
                    specs {
                        attribute {
                            name
                        }
                        value
                        units
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

def query_bom(queries):
    response = nexar.get_query(multi_match, {
        "queries": queries
    })
    return response.get("supMultiMatch")

def get_similar_parts(mpn, manufacturer):
    response = nexar.get_query(similar_parts, {
        "mpn": mpn,
        "manufacturer": manufacturer
    })
    return response.get("supMultiMatch")[0].get("parts")[0].get("similarParts")

def get_spec(specs, spec_name):
    for spec in specs:
        if spec.get("attribute").get("name") == spec_name:
            return spec.get("value")
    return None