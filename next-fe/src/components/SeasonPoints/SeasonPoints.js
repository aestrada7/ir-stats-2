import Classes from "./SeasonPoints.module.scss";
import { calculateSeasonPoints } from "@/services/scoring";

export default function SeasonPoints(props) {
    const { sessions } = props;
    sessions.sort((a, b) => b.race_week_num - a.race_week_num);
    const pointsInfo = calculateSeasonPoints(sessions);

    return (
        <div className={Classes.seasonPoints}>
            <div className={Classes.pointsHeader}>Points</div>
            <div className={Classes.boxData}>
                { pointsInfo.weeks.map(weekData => (
                    <div key={weekData.week} className={[Classes.singleStat, weekData.inUse ? Classes.inUse : ''].join(' ')}> 
                        <div className={Classes.statTitle}>
                            W{weekData.week + 1} - {weekData.track_id}
                        </div>
                        <div className={Classes.statValue}>{weekData.weekPoints}</div>
                    </div>
                ))}
            </div>
        </div>
    )
}