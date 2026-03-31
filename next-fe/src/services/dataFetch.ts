import { PYRA_BASE_URL } from "@/services/config";
import { Season } from "@/services/interfaces";

const REVALIDATE_TIME: number = 3600;

/**
 * Retrieves all existing seasons stored in the database.
 * 
 * @param cust_id The customer id to filter by.
 * @param series_id The series id to filter by.
 * @returns The JSON object with all recorded seasons for the filtered combination.
 */
export const getSeasonList = async(cust_id: number, series_id: number): Promise<Season[]> => {
    const response = await fetch(`${PYRA_BASE_URL}/seasons?cust_id=${cust_id}&series_id=${series_id}`, {
        next: { revalidate: REVALIDATE_TIME }
    });
    const data: Season[] = await response.json();
    return data;
}

/**
 * Retrieves all existing sessions stored in the database for a particular season quarter.
 * 
 * @param {number} cust_id The customer id to filter by.
 * @param {number} series_id The series id to filter by.
 * @param {number} season_year The season year to filter by.
 * @param {number} season_quarter The season quarter to filter by.
 * @returns {object} The JSON object with all recorded sessions for the filtered combination.
 */
export const getSeasonSessions = async(cust_id, series_id, season_year, season_quarter) => {
    const response = await fetch(`${PYRA_BASE_URL}/season_sessions?cust_id=${cust_id}&series_id=${series_id}&season_year=${season_year}&season_quarter=${season_quarter}`, {
        next: { revalidate: REVALIDATE_TIME }
    });
    return await response.json();
}