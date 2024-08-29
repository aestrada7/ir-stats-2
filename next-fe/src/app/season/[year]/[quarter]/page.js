import SeasonTable from "@/components/SeasonTable/SeasonTable";
import StatsBox from "@/components/StatsBox/StatsBox";
import { getSeasonSessions } from "@/services/dataFetch";

export default async function Page({ params }) {
    const year = params?.year;
    const quarter = params?.quarter;

    const seasonSessions = await getSeasonSessions(182407, 132, year, quarter);
    seasonSessions.reverse();

    return (
        <div>
            <StatsBox sessions={seasonSessions} />
            <SeasonTable sessions={seasonSessions} />
        </div>
    );
}