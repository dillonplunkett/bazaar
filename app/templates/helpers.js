{% macro autocomplete(field, options) %}
    function case_insens_sort(a, b) {
        var a_low = a.toLowerCase();
        var b_low = b.toLowerCase()
        if (a_low < b_low) return -1;
        if (a_low > b_low) return 1;
        return 0;
    }
    var options = JSON.parse('{{ options|tojson }}').sort(case_insens_sort);
    $("#{{ field }}").autocomplete({
        source: function(request, response) {
            var results = $.ui.autocomplete.filter(options, request.term);
            response(results.slice(0, 10));
        },
        autoFocus: true
    });
{% endmacro %}
