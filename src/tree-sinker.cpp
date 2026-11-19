// C headers
#include <argp.h>
#include <curl/curl.h>
#include <curl/curlver.h>

// C++ headers
#include <iostream>
#include <print>

const char *argp_program_version =
    "tree-sinker 0.5 compiled against libcurl " LIBCURL_VERSION;
const char *argp_program_bug_address = "<robert@rrbrussell.com>";
const char *doc = "tree-sinker -- a tool for synchronizing portage tree "
                  "snapshots archived with squashfs.";
const char args_doc[] = "REPOSITORY_NAME";
const unsigned NUMBER_OF_REPOS_WE_CAN_PROCESS_AT_ONCE = 1;
struct arguments {
  char *repository_name;
};

error_t parse_opt(int key, char *arg, struct argp_state *state) {
  struct arguments *arguments = static_cast<struct arguments *>(state->input);
  switch (key) {
  case ARGP_KEY_ARG: {
    if (NUMBER_OF_REPOS_WE_CAN_PROCESS_AT_ONCE == (state->arg_num + 1)) {
      arguments->repository_name = arg;
    } else {
      argp_usage(state);
    }
  } break;
  case ARGP_KEY_END: {
    if (state->arg_num != NUMBER_OF_REPOS_WE_CAN_PROCESS_AT_ONCE) {
      argp_usage(state);
    } else {
      break;
    }
  }
  default: {
    return ARGP_ERR_UNKNOWN;
  }
  }
  return 0;
}

const struct argp argp = {0, parse_opt, args_doc, doc};

int main(int argc, char *argv[]) {
  /* Begin argument processing */
  struct arguments arguments = {.repository_name = nullptr};
  argp_parse(&argp, argc, argv, 0, 0, &arguments);
  std::cout << "The repo i will process is " << arguments.repository_name
            << std::endl;
  /* End of argument processing */

  /* Setup curl */
  CURLcode result_code = curl_global_init(CURL_GLOBAL_DEFAULT);
  if (result_code != CURLE_OK) {
    std::println(std::cerr,
                 "Unable to initalize the curl library. "
                 "Please use the error message below for troubleshooting.");
    std::cerr << curl_easy_strerror(result_code) << std::endl;
  }

  /* End of program cleanup */
  curl_global_cleanup();
  return EXIT_SUCCESS;
}
