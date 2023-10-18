# Sample Materials, provided under license.
# Licensed Materials - Property of IBM
# Â© Copyright IBM Corp. 2019, 2020. All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

# Inputs
#hostname <- 'https://zen-cpd-zen.apps.ka-accelerator-test-35h.os.fyre.ibm.com'
#username <- 'admin'
#password <- 'password'


library(httr)
library(rjson)


collectDeployments <- function(hostname, username, password, target_tag=NULL) {
  
  if (isTRUE(startsWith(hostname, "https://"))) {
    base_url <- hostname
  } else {
    base_url <- sprintf('https://%s', hostname)
  }
  
  if (isTRUE(endsWith(base_url, "/"))) {
    base_url <- sub("/$", "", base_url)
  } 

  authResponse = httr::content(GET(url=paste(base_url, '/v1/preauth/validateAuth',sep=''),
                             authenticate(username, password),
                             httr::config(ssl_verifyhost = FALSE, ssl_verifypeer = FALSE)))
  

  if("accessToken" %in% names(authResponse)) {
    token <- authResponse$accessToken
  } else if("message" %in% names(authResponse)) {
    stop(paste("ERROR:", authResponse$message))
  } else {
    stop(paste("ERROR:", authResponse))
  }
  
  spaces <- httr::content(GET(url=paste(base_url,'/v2/spaces',sep=''),
                        httr::config(ssl_verifyhost = FALSE, ssl_verifypeer = FALSE),
                        add_headers(Authorization = paste('Bearer', token)),
                        encode="json"))$resources
  

  spaceNames = list()
  for(space in spaces) {
    spaceNames[[space$metadata$id]] = space$entity$name
  }
  
  
  validDeployments <- list()
  errorMsg <- list("ERROR: No valid deployments found.", " ")
  deployment_url=paste0(paste0(base_url,"/ml/v4/deployments?version="),Sys.Date())
  
  deployments <- httr::content(GET(url=deployment_url,
                             httr::config(ssl_verifyhost = FALSE, ssl_verifypeer = FALSE),
                             add_headers(Authorization = paste('Bearer', token)),
                             encode="json"))$resources
  

  for(deployment in deployments) {
    if(length(target_tag) == 0 || (length(deployment$entity$name) > 0 && deployment$entity$name == target_tag )) {
      
      # select a unique index name for the deployment
      index_name = deployment$entity$name
      i = 1
      while(index_name %in% names(validDeployments)) {
        i = i + 1
        index_name = paste0(deployment$entity$name, ' (', i, ')')
      }
      
      # populate deployment info
      space_guid = deployment$entity$space_id#strsplit(deployment$entity$space$href, '/')[[1]][[4]]
      validDeployments[[index_name]] = list(
        guid = deployment$metadata$id, 
        space_id = space_guid, 
        space_name = spaceNames[[space_guid]],
        #tags = paste(lapply(deployment$entity$tags, function(x) x$value), collapse=', '),
        scoring_url = deployment$entity$status$online_url$url
      )
    }
  }
  
  if(length(validDeployments) == 0) {
    errorMsg <- c(errorMsg, paste0("Make sure you have Developer or Admin access to a Project Release with a deployment tagged with '",target_tag,"'"))
    stop(paste(errorMsg, collapse='\n'))
  }
  return(list(token=token, deployments=validDeployments))
}



scoreModelDeployment <- function(scoring_url, data, token) {
  
  scoring_url=paste0(paste0(scoring_url,"?version="),Sys.Date())
  print(scoring_url)
  print(data)
  resp <- httr::content(POST(url = scoring_url,
                       httr::config(ssl_verifyhost = FALSE, ssl_verifypeer = FALSE),
                       add_headers(Authorization = paste('Bearer', token)),
                       body = list(input_data = list(data)),
                       encode = "json",
                       timeout(8)))
  
  if(length(resp$predictions) > 0) {
    return(resp)
  } else if(length(resp$stderr) > 0) {
    return(list(error=resp$stderr))
  } else {
    return(list(error=resp))
  }
}







