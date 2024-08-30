const SEASON_LEAP_WEEKS = 9;
const SEASON_WEEKS = 8;
const SEASON_MAX_WEEKS = 12;
const RACE_PERCENT = 0.25;

/**
 * Performs a calculation of season's points given a set of race data.
 * 
 * @param {object} raceData A subset of the race data encompassing a single season.
 * @returns {object} An object with the total points earned in a season as well as its detailed view.
 */
export const calculateSeasonPoints = (raceData) => {
    let pointsObj = {
        totalPoints: 0,
        weeks: []
    };

    //determines if a season is leap or not
    const maxWeeks = raceData[0].max_weeks === SEASON_MAX_WEEKS ? SEASON_WEEKS : SEASON_LEAP_WEEKS;

    const weeksRaced = [...new Set(raceData.map(item => item.race_week_num))];
    pointsObj.weeks.push(...weeksRaced.map(weekItem => calculateWeekPoints(raceData, weekItem)));

    pointsObj.weeks = pointsObj.weeks.sort((a, b) => b.weekPoints - a.weekPoints);
    pointsObj.weeks.map((item, idx) => idx < maxWeeks ? item.inUse = true : '');
    pointsObj.weeks = pointsObj.weeks.sort((a, b) => b.week - a.week);
    pointsObj.totalPoints = pointsObj.weeks.filter(x => x.inUse).reduce((acc, tot) => acc + tot.weekPoints, 0);

    return pointsObj;
};

/**
 * Performs a calculation to determine the total points earned in a single week, according to the sporting code
 * set by iRacing.
 * 
 * @param {object} raceData An subset of the race data encompassing a single season.
 * @param {number} week The week number.
 * @returns {object} An object with the week data.
 */
export const calculateWeekPoints = (raceData, week) => {
    const filteredData = raceData.filter(item => item.race_week_num === week);
    const track_id = filteredData[0].track_id;
    const filteredPoints = filteredData.map(item => item.champ_points).sort((a, b) => b - a);
    const racesToAverage = Math.ceil(filteredPoints.length * RACE_PERCENT);
    const weekPoints = filteredPoints.reduce((acc, tot, idx) => idx < racesToAverage ? acc + tot : acc, 0) / racesToAverage;

    return { weekPoints, week, inUse: false, track_id };
};