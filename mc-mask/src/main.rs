use rcon::{self, Connection};
use regex::Regex;
use std::error::Error;

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
    if std::env::args().len() != 4 {
        println!(
            "Usage: {} <server> <rcon-password> <user>",
            std::env::args().nth(0).unwrap(),
        );
        return Ok(());
    }
    let addr = std::env::args().nth(1).unwrap();
    let password = std::env::args().nth(2).unwrap();
    let user = std::env::args().nth(3).unwrap();
    let mut conn = Connection::connect(&addr, &password)?;
    let (x, y, z) = block_below_player(&mut conn, &user)?;
    let cmd = format!("setblock {} {} {} gold_block", x, y, z);
    conn.cmd(&cmd)?;
    Ok(())
}
