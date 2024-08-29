import Classes from "./StatsBox.module.scss";
import { statsBoxDataBuild } from "@/services/stats";

export default function StatsBox(props) {
    let { sessions } = props;
    let boxData = statsBoxDataBuild(sessions);

    return (
        <div className={Classes.statsBox}>
            <div className={Classes.boxHeader}>Stats</div>
            <div className={Classes.boxData}>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Races</div>
                    <div className={Classes.statValue}>{boxData.races}</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Total Laps</div>
                    <div className={Classes.statValue}>{boxData.totalLaps}</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Wins</div>
                    <div className={Classes.statValue}>{boxData.wins} ({boxData.winPercentage}%)</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Laps Led</div>
                    <div className={Classes.statValue}>{boxData.lapsLed}</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Top 5s</div>
                    <div className={Classes.statValue}>{boxData.top5s} ({boxData.top5Percentage}%)</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Laps Completed</div>
                    <div className={Classes.statValue}>{boxData.actualLaps} ({boxData.actualLapsPercentage}%)</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Top 10s</div>
                    <div className={Classes.statValue}>{boxData.top10s} ({boxData.top10Percentage}%)</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Average Start</div>
                    <div className={Classes.statValue}>{boxData.avgStart}</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Poles</div>
                    <div className={Classes.statValue}>{boxData.poles}</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Average Finish</div>
                    <div className={Classes.statValue}>{boxData.avgFinish}</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Best Result</div>
                    <div className={Classes.statValue}>{boxData.bestResult}</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>Avg Fin (No DNF)</div>
                    <div className={Classes.statValue}>{boxData.avgFinishSansDnfs}</div>
                </div>
                <div className={Classes.singleStat}>
                    <div className={Classes.statTitle}>DNFs</div>
                    <div className={Classes.statValue}>{boxData.dnfs} ({boxData.dnfPercentage}%)</div>
                </div>
            </div>
        </div>
    )
}