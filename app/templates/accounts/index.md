<center><h2>[Home](/)</h2></center>

{% if not account_name %}
    <title>Accounts</title>
    <h1>Accounts</h1>
    {{accounts|safe}}
{% else %}
    <title>Accounts | {{account_name}}</title>
    <h1><a href="/accounts">Accounts</a></h1>
    {{account|safe}}
{% endif %}

<script>
    var _delete = function() {
        console.log({{account[0]}});
        var ajax = new XMLHttpRequest();
        ajax.open("POST", "/accounts/{{account[0]}}", true);
        ajax.send();
    }
</script>
