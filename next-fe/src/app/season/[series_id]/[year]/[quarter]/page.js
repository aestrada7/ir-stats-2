import SeasonTable from "@/components/SeasonTable/SeasonTable";
import StatsBox from "@/components/StatsBox/StatsBox";
import SeasonPoints from "@/components/SeasonPoints/SeasonPoints";
import { getSeasonSessions } from "@/services/dataFetch";

import Classes from "@/scss/Main.module.scss";

export default async function Page({ params }) {
    const series_id = params?.series_id;
    const year = params?.year;
    const quarter = params?.quarter;

    const seasonSessions = await getSeasonSessions(182407, series_id, year, quarter);
    seasonSessions.reverse();

    return (
        <div>
            <div className={Classes.globalSideBySide}>
                <StatsBox sessions={seasonSessions} />
                <SeasonPoints sessions={seasonSessions} />
            </div>
            <SeasonTable sessions={seasonSessions} />
        </div>
    );
}