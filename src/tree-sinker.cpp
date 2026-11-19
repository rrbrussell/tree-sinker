// C headers
#include <argp.h>
#include <curl/curl.h>
#include <curl/curlver.h>
#include <errno.h>
#include <stdlib.h>

// C++ headers
#include <filesystem>
#include <format>
#include <functional>
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

/*
 * I can either find a C++ native way to handle this mess or create my own
 * wrapper class.
 */
static char temporary_directory_template[] = "/var/tmp/tree_sinker.XXXXXX";
static char *created_temporary_directory_name = nullptr;
void cleanup_temporary_directory() {
  std::filesystem::path temporary_directory =
      std::filesystem::path(created_temporary_directory_name);
  std::filesystem::remove_all(temporary_directory);
}

using std::cerr;
using std::cout;
using std::endl;
using std::println;

int main(int argc, char *argv[]) {
  /* Begin argument processing */
  struct arguments arguments = {.repository_name = nullptr};
  argp_parse(&argp, argc, argv, 0, 0, &arguments);
  cout << "The repo i will process is " << arguments.repository_name << endl;
  /* End of argument processing */

  created_temporary_directory_name = mkdtemp(temporary_directory_template);
  if (created_temporary_directory_name == nullptr) {
    println(cerr, "Unable to create a temporary directory named {:s}",
            temporary_directory_template);
    switch
      errno {
      case EACCES: {
        println(cerr, "No write permissions to /var/tmp.");
        break;
      }
      case EEXIST: {
        println(cerr, "The temporary directory already exists or a file exists "
                      "with the same name as the temporary directory in "
                      "/var/tmp.");
        break;
      }
      case EMLINK: {
        println(cerr, "/var/tmp cannot have any more entries.");
        break;
      }
      case ENOSPC: {
        println(cerr, "/var/tmp is full or on a full filesystem.");
        break;
      }
      case EROFS: {
        println(cerr, "/var/tmp is read only or on a read only filesystem.");
        break;
      }
      default: {
        println(cerr, "The error type isn't known to tree-sinker here is what "
                      "libc thinks happened.");
        perror(nullptr);
      }
      }
    exit(EXIT_FAILURE);
  }
  atexit(&cleanup_temporary_directory);

  /* Setup curl */
  CURLcode result_code = curl_global_init(CURL_GLOBAL_DEFAULT);
  if (result_code != CURLE_OK) {
    println(cerr, "Unable to initalize the curl library. "
                  "Please use the error message below for troubleshooting.");
    cerr << curl_easy_strerror(result_code) << endl;
  }
  atexit(&curl_global_cleanup);

  /* End of program cleanup */
  return EXIT_SUCCESS;
}
