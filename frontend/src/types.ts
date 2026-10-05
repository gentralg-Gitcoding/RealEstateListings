export interface Listing {
    id: string;
    source: string;
    address: string;
    city: string;
    state: string;
    zip: string;
    price: number;
    bedrooms: number;
    bathrooms: number;
    sqft: number;
    latitude: number;
    longitude: number;
    listedDate: string;
    status: "active" | "pending" | "sold";
    description: string;
}

export interface SearchParams {
    minPrice?: number;
    maxPrice?: number;
    minBeds?: number;
    city?: string;
    keyword?: string;
    targetBudget?: number;
    page?: number;
    pageSize?: number;
}

export interface SearchResult {
    data: (Listing & {score: number})[];
    total: number;
    page: number;
    pageSize: number;
    error?: string;
}
