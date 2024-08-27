import SessionInfo from "@/components/SessionInfo/SessionInfo";
import { getSeasonSessions } from "@/services/dataFetch";

import Classes from "@/app/season/Season.module.scss";

export default async function Page({ params }) {
    const year = params?.year;
    const quarter = params?.quarter;

    const seasonSessions = await getSeasonSessions(182407, 132, year, quarter);
    seasonSessions.reverse();

    return (
        <div className={Classes.season}>
            <div className={Classes.seasonHeader}>
                <div className={Classes.largeHeader}>Track / Date / Winner</div>
                <div className={Classes.simpleHeader}>Points</div>
                <div className={Classes.simpleHeader}>Laps/Total</div>
                <div className={Classes.simpleHeader}>Led</div>
                <div className={Classes.simpleHeader}>Start</div>
                <div className={Classes.simpleHeader}>Finish</div>
            </div>
            { seasonSessions.map((session) => (
                <SessionInfo key={`${session.session_id}`} session={session}></SessionInfo>
            ))}
        </div>
    );
}