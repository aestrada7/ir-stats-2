import MenuCard from "@/components/MenuCard/MenuCard";
import { getSeasonList } from "@/services/dataFetch";

export default async function Page() {
    const seasonList = await getSeasonList(182407, 132);

    return (
        <div>
            { seasonList.map((season) => (
                <MenuCard key={`${season.season_year}-${season.season_quarter}`} 
                          link={`/season/${season.season_year}/${season.season_quarter}`}
                          caption={`${season.season_year} Season ${season.season_quarter}`} />
            ))}
        </div>
    );
}