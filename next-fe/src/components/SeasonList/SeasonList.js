import MenuCard from "@/components/MenuCard/MenuCard";
import { getSeasonList } from "@/services/dataFetch";

import Classes from "./SeasonList.module.scss";

export default async function SeasonList(props) {
    const { seriesObj } = props;
    const { cust_id } = props;

    let allSeasonsList = [];

    for(let i in seriesObj.series) {
        let tempList = await getSeasonList(cust_id, seriesObj.series[i].series_id);
        for(let k in tempList) {
            tempList[k]["series_id"] = seriesObj.series[i].series_id;
        }
        allSeasonsList = allSeasonsList.concat(tempList);
    }

    /**
     * Needed to add all these comparisons since iRacing decided to reuse the same series_id for different seasons.
     * Indy Fixed Oval was 165 forever and they changed it to 132, which was a deprecated series.
     * 
     * This also meant that the new Indy Fixed Sprint would hold all the old data of the 165 series.
     * Hacky, but works
     * */
    let filteredList = allSeasonsList.filter((season) => {
        for(let i in seriesObj.series) {
            if(season.series_id === seriesObj.series[i].series_id) {
                let serializedYQ = parseInt(`${season.season_year}${season.season_quarter}`);
                if(seriesObj.series[i].from_season_yq) {
                    if(serializedYQ < seriesObj.series[i].from_season_yq) {
                        return false;
                    }
                }
                if(seriesObj.series[i].to_season_yq) {
                    if(serializedYQ > seriesObj.series[i].to_season_yq) {
                        return false;
                    }
                }
            }
        }
        return true;
    });

    let seasonList = filteredList.sort((a, b) => parseInt(`${b.season_year}${b.season_quarter}`) - parseInt(`${a.season_year}${a.season_quarter}`));

    return (
        <div className={Classes.seasonList}>
            <div className={Classes.seasonTitle}>
                {seriesObj.series_title}
                <span className={Classes.syncIcon}>sync</span>
            </div>
            <div className={Classes.seasonSyncWindow}>
                <div className={Classes.seasonSyncTitle}>Season Sync: {seriesObj.series_title}</div>
                <div className={Classes.seasonSyncClose}>x</div>
            </div>
            {
                seasonList.length === 0 ? <div className={Classes.noSeasons}>No seasons found</div> : null
            }
            <div className={Classes.seasons}>
                { seasonList.map((season) => (
                    <MenuCard key={`${season.season_year}-${season.season_quarter}`} 
                              link={`/season/${season.series_id}/${season.season_year}/${season.season_quarter}`}
                              caption={`${season.season_year} Season ${season.season_quarter}`} />
                ))}
            </div>
        </div>
    )
}