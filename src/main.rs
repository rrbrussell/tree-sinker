#![allow(unused)]

use std::collections::HashMap;
use std::fs::File;
use std::fs::Metadata;
use std::fs::symlink_metadata;
use std::io::prelude::*;
use std::io::BufReader;
use std::io::Error;
use std::path::Path;
use std::process::exit;

use strfmt::strfmt;

fn main() {
    //static HEADER_TEXT: &str = include_str!("tree_sinker_header.txt");
    //let mut vars = HashMap::with_capacity(2);
    //vars.insert("YEAR".to_string(), "2026".to_string());
    //vars.insert("AUTHORS".to_string(), env!("CARGO_PKG_AUTHORS").to_string());
    //match strfmt(HEADER_TEXT, &vars) {
    //    Ok( s ) => {
    //        print!("{}", s);
    //    }
    //    Err(e) => {
    //        eprintln!("Please file a bug for this. {} {}", file!(), line!());
    //        eprintln!("{e:?}");
    //    }
    //}

    println!("{:?}", read_configuration());

}

#[derive(Debug)]
struct Configuration<'a> {
    file: &'a Path,
    server: String,
    path: String,
    repos_dir: String,
}

fn read_configuration<'a>() -> Option<Configuration<'a>> {
    let mut maybe_server: Option<String> = None;
    let mut maybe_path: Option<String> = None;
    let mut maybe_repos_dir: Option<String> = None;
    let file_path: &Path = Path::new("etc/tree-sinker.ini");
    let temp = File::open(file_path);
    let m: Metadata;
    let reader: BufReader<File>;
    match temp {
        Ok(_f) => {
            match _f.metadata() {
                Ok(_m) => {
                    m = _m;
                }
                Err(_) => {
                    return None;
                }
            }
            reader = BufReader::new(_f);
        }
        Err(_) => {
            return None;
        }
    }
    if m.len() >= CONFIG_FILE_TO_BIG_LIMIT {
        eprintln!("{}", CONFIG_FILE_TO_BIG_MESSAGE);
        return None;
    }
    if m.len() == CONFIG_FILE_TO_SMALL_LIMIT {
        eprintln!("{}", CONFIG_FILE_TO_SMALL_MESSAGE);
        return None;
    }
    drop(m);
    let mut lines: Vec<String> = reader.lines().map(|l| l.unwrap()).collect();
    let mut indexes: Vec<usize> = Vec::with_capacity(lines.len());
    for (index, line) in lines.iter().enumerate() {
        if line.trim().is_empty() {
            indexes.push(index);
            continue;
        }
        if line.trim().starts_with("#") {
            indexes.push(index);
            continue;
        }
    }
    for index in indexes.into_iter().rev() {
        lines.remove(index);
    }

    lines.sort();
    
    for line in lines {
        let temp_line = line.trim();
        match temp_line.split_once("=") {
            Some((key, value)) => {
                let key = key.trim();
                let value = value.trim();
                if key.is_empty() || value.is_empty() {
                    eprint!("{temp_line}\nIs malformed. ");
                    if key.is_empty() {
                        eprint!("The configuration keys are: server, path, and repos_dir.");
                        return None;
                    } else {
                        eprintln!("There is no configuration value after the key.");
                        if key.eq("server") {
                            eprint!("A server configuration statement expects");
                            eprintln!(" http://HOSTNAME or https://HOSTNAME.");
                        } else {
                            if key.eq("path") {
                                eprint!("A path configuration statement");
                                eprint!(" expects a path which will be");
                                eprint!(" concatenated with the server");
                                eprintln!(" statement.");
                            } else {
                                if key.eq("repos_dir") {
                                eprint!("A repos_dir configuration statement");
                                eprint!(" expects an absolute local directory");
                                    eprintln!(" path.");
                                } else {
                                    eprint!("Unknown configuration statement");
                                    eprintln!(" key {key}.");
                                }
                            }
                        }
                    }
                }
                if key.eq("path") {
                    maybe_path = Some(value.to_owned());
                    continue;
                } else if key.eq("repos_dir") {
                    maybe_repos_dir = Some(value.to_owned());
                    continue;
                } else if key.eq("server") {
                    maybe_server = Some(value.to_owned());
                    continue;
                } else {
                    eprint!("{key} = {value} is not a valid configuration ");
                    eprint!("statement.\n{key} is not one of server, path, ");
                    eprintln!("or repos_dir.");
                    return None;
                }
            }
            None => {
                let mut vars = HashMap::with_capacity(2);
                vars.insert("fp".to_string(), file_path.to_string_lossy().to_string());
                vars.insert("line".to_string(), temp_line.to_string());
                match strfmt(CONFIG_FILE_LINE_NO_EQUALS, &vars) {
                    Ok( s ) => {
                        print!("{}", s);
                    }
                    Err(e) => {
                        eprintln!("Please file a bug for this. {} {}",
                            file!(), line!());
                        eprintln!("{e:?}");
                    }
                }
                return None;
            }
        }
    }

    match (maybe_server, maybe_path, maybe_repos_dir) {
        (Some(server), Some(path), Some(repos_dir)) => {
            return Some(Configuration{
                file: file_path,
                server, path, repos_dir
            });
        }
        (_, _, _) => {
            return None;
        }
    }
}

static CONFIG_FILE_LINE_NO_EQUALS: &str =
"Found an incorrect line in configuration file: {fp}.
{line}\nshould have an \"=\" in it. It does not.";
static CONFIG_FILE_TO_BIG_LIMIT: u64 = 1*1024*1024;
static CONFIG_FILE_TO_BIG_MESSAGE: &str =
"The configuration file is larger than 1MiB. It shouldn't be that large.";
static CONFIG_FILE_TO_SMALL_LIMIT: u64 = 0;
static CONFIG_FILE_TO_SMALL_MESSAGE: &str =
"The configuration file is empty. Please fix.";
