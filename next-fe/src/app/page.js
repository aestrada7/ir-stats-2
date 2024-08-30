import SeasonList from "@/components/SeasonList/SeasonList";
import { IR_STATS_SERIES } from "@/services/series";

export default async function Page() {
    //let series = await getSeries(182407);

    return (
        <div>
            { IR_STATS_SERIES.map((series) => (
                <SeasonList key={series.ir_id} seriesObj={series} />
            )) }
        </div>
    );
}