use std::fs::File;
use std::fs::Metadata;
use std::io::prelude::*;
use std::io::Error;
use std::process::exit;

fn main() {
    println!("Test program.");
    let temp = File::open("testfile");
    let f: File;
    match temp {
        Ok(_f) => {
            println!("testfile can be read.");
            f = _f;
        }
        Err(e) => {
            println!("{e:?}");
            exit(1);
        }
    }
    let temp = f.metadata();
    let m: Metadata;
    match temp {
        Ok(_m) => {
            println!("testfile's metadata can be read.");
            m = _m;
        }
        Err(e) => {
            println!("{e:?}");
            exit(1);
        }
    }
    println!("Testfile is {:x} bytes in length", m.len());
}
