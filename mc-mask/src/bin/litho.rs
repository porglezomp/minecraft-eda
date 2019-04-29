use rcon::{self, Connection};
use regex::Regex;
use std::{
    error::Error,
    io::{self, BufRead},
    env,
};

fn block_below_player(conn: &mut Connection, user: &str)
    -> Result<(i32, i32, i32), Box<dyn Error>>
 {
    let cmd = format!("execute at {user} run tp {user} ~ ~ ~", user=user);
    let text = conn.cmd(&cmd)?;
    let re = Regex::new(r"Teleported .* to (.*), (.*), (.*)").unwrap();
    if let Some(cap) = re.captures(&text) {
        let x = (cap[1].parse::<f32>()? + 0.0) as i32;
        let y = (cap[2].parse::<f32>()? - 1.0) as i32;
        let z = (cap[3].parse::<f32>()? - 1.0) as i32;
        Ok((x, y, z))
    } else {
        Err(text)?
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    if let [_, addr, pass, user] = &env::args().collect::<Vec<_>>()[..] {
        let mut conn = Connection::connect(&addr, &pass)?;
        let (x0, y0, z0) = block_below_player(&mut conn, &user)?;
        println!("Placing design at player {}, at {} {} {}", user, x0, y0, z0);
        println!("Reading commands on stdin");
        for (i, line) in io::stdin().lock().lines().enumerate() {
            let line = line?;
            let mut parts = line.split_whitespace();
            let x = parts.next().ok_or("Missing x")?.parse::<i32>()?;
            let y = parts.next().ok_or("Missing y")?.parse::<i32>()?;
            let z = parts.next().ok_or("Missing z")?.parse::<i32>()?;
            let block = parts.next().ok_or("Missing block name")?;
            if let Some(txt) = parts.next() {
                println!("Warning: Unexpected trailing {} on line {}", txt, i);
            }
            // We shuffle y and z in input coordinates in order to make coordinates good :3
            conn.cmd(&format!("setblock {} {} {} {}", x0 + x, y0 + z, z0 + y, block))?;
        }
        Ok(())
    } else {
        println!(
            "Usage: {} <server> <rcon-password> <user>",
            env::args().nth(0).unwrap(),
        );
        Ok(())
    }
}
