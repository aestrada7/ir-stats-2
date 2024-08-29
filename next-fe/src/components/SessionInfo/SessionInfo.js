import { formatDateTime } from "@/services/common";
import Classes from "./SessionInfo.module.scss";

export default function SessionInfo(props) {
    let { session } = props;
    let startClasses = [Classes.start, Classes['p' + session.starting_position]].join(' ');
    let finishClasses = [Classes.finish, Classes['p' + session.finishing_position]].join(' ');

    return (
        <div className={Classes.sessionInfo}>
            <div className={Classes.sessionData}>
                <div className={Classes.week}>Week {session.race_week_num + 1}</div>
                <div className={Classes.track}>{session.track_id}</div>
                <div className={Classes.date}>{formatDateTime(session.start_time)}</div>
                <div className={Classes.winner}>{session.winner_name}</div>
                { 
                    // <Driver id={session.winner_id} color1={session.winner_color1} color2={session.winner_color2} color3={session.winner_color3} name={session.winner_name} /> // 
                }
            </div>
            <div className={Classes.sof}>{session.sof}</div>
            <div className={Classes.points}>{session.champ_points}</div>
            <div className={Classes.laps}>{session.laps}/{session.event_laps_complete}</div>
            <div className={Classes.led}>{session.led}</div>
            <div className={startClasses}>{session.starting_position}</div>
            <div className={finishClasses}>{session.finishing_position}</div>
        </div>
    )
}