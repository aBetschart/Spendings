
$(document).ready(function () {
    

});


async function getCategories() {
    try {
        const data = await $.ajax({
            type: "GET",
            url: DJANGO_URLS.category_get,
        });
        return data.categories;
    }
    catch (error) {
        console.error("Error fetching categories:", error);
        throw new Error("Failed to fetch categories");
    }
}