window.addEventListener("DOMContentLoaded", function() {
    const params = new URLSearchParams(window.location.search);
    const search_filter = params.get('text') || '';
    if (search_filter.length > 1) {
        $(".quote-text").highlight(search_filter)
    }
}, false);