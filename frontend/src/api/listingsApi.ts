import type { SearchParams, SearchResult } from "../types";

const API_URL = import.meta.env.VITE_API_URL;

export async function fetchListings (
    params: SearchParams
): Promise<SearchResult> {
    const queryParams = new URLSearchParams();

    if (params.minPrice !== undefined) {
        queryParams.set("minPrice", String(params.minPrice));
    }

    if (params.maxPrice !== undefined) {
        queryParams.set("maxPrice", String(params.maxPrice));
    }

    if (params.minBeds !== undefined) {
        queryParams.set("minBeds", String(params.minBeds));
    }

    if (params.city !== undefined) {
        queryParams.set("city", String(params.city));
    }

    if (params.keyword !== undefined) {
        queryParams.set("keyword", String(params.keyword));
    }

    if (params.targetBudget !== undefined) {
        queryParams.set("targetBudget", String(params.targetBudget));
    }

    if (params.page !== undefined) {
        queryParams.set("page", String(params.page));
    }

    if (params.pageSize !== undefined) {
        queryParams.set("pageSize", String(params.pageSize));
    }

    // Build the url with query params
    const response = await fetch (
        `${API_URL}/listings?${queryParams.toString()}`
    );

    if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
    }

    return await response.json()
}