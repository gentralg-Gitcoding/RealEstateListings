import { useEffect, useState } from "react";
import { SearchResult } from "./types.ts";
import { fetchListings } from "./api/listingsApi.ts";

function App() {
    const [minPrice, setMinPrice] = useState("");
    const [maxPrice, setMaxPrice] = useState("");
    const [minBeds, setMinBeds] = useState("");
    const [city, setCity] = useState("");
    const [keyword, setKeyword] = useState("");
    const [targetBudget, setTargetBudget] = useState("");
    const [page, setPage] = useState("");
    const [pageSize, setPageSize] = useState("");
    const [result, setResult] = useState<SearchResult>({
        data: [],
        total: 0,
        page: 1,
        pageSize: 10,
    });

    useEffect(() => {
        const loadListings = async () => {
            try {
                const result = await fetchListings({
                    minPrice: minPrice ? Number(minPrice) : undefined,
                    maxPrice: maxPrice ? Number(maxPrice) : undefined,
                    minBeds: minBeds ? Number(minBeds) : undefined,
                    city: city || undefined,
                    keyword: keyword || undefined,
                    targetBudget: targetBudget ? Number(targetBudget) : undefined,
                    page: page ? Number(page) : undefined,
                    pageSize: pageSize ? Number(pageSize) : undefined
                });

                setResult(result);

            } catch (error) {
                console.error(`Failed to load listings: ${error}`);
            }
        };

        loadListings()

    }, [
        minPrice,
        maxPrice,
        minBeds,
        city,
        keyword,
        targetBudget,
        page,
        pageSize
    ]);


    return (
        <div>

            <h1>Rental Listings</h1>

            <div>
                <input
                    type="number"
                    placeholder="Min Price"
                    value={minPrice}
                    onChange={(e) =>
                        setMinPrice(e.target.value)
                    }
                />
                <input
                    type="number"
                    placeholder="Max Price"
                    value={maxPrice}
                    onChange={(e) =>
                        setMaxPrice(e.target.value)
                    }
                />
                <input
                    type="number"
                    placeholder="Minimum Beds"
                    value={minBeds}
                    onChange={(e) =>
                        setMinBeds(e.target.value)
                    }
                />
                <input
                    type="text"
                    placeholder="City"
                    value={city}
                    onChange={(e) =>
                        setCity(e.target.value)
                    }
                />
                <input
                    type="text"
                    placeholder="Keyword"
                    value={keyword}
                    onChange={(e) =>
                        setKeyword(e.target.value)
                    }
                />
                <input
                    type="number"
                    placeholder="TargetBudget"
                    value={targetBudget}
                    onChange={(e) =>
                        setTargetBudget(e.target.value)
                    }
                />
                <input
                    type="number"
                    placeholder="Page"
                    value={page}
                    onChange={(e) =>
                        setPage(e.target.value)
                    }
                />
                <input
                    type="number"
                    placeholder="PageSize"
                    value={pageSize}
                    onChange={(e) =>
                        setPageSize(e.target.value)
                    }
                />
                
            </div>

            <h2>
                {result.total} Listings Found
            </h2>

            {result.error && (
                <p>{result.error}</p>
            )}

            <div>
                {result.data.map((listing) => (

                    <div key={listing.id}>

                        <h2>
                            ${listing.price.toLocaleString()}
                        </h2>

                        <h3>
                            {listing.address}
                        </h3>

                        <p>
                            {listing.city}, {listing.state}{" "}{listing.zip}
                        </p>
                        <p>
                            Lat: {listing.latitude} - Long: {listing.longitude}
                        </p>

                        <p>
                            {listing.bedrooms} beds -{" "}
                            {listing.bathrooms} baths -{" "}
                            {listing.sqft} sqft
                        </p>

                        <p>
                            {listing.description}
                        </p>
                        <p>
                            Listing Date: {listing.listedDate}
                        </p>

                        <small>
                            Match score:{" "}
                            {listing.score.toFixed(2)}
                        </small>

                        <hr />

                    </div>

                ))}
            </div>

        </div>
    );
}

export default App;