<center><h2>[Home](/)</h2></center>

# [Accounts](/accounts)

{% if not account_name %}
    <h2>Add an account</h2>
    <form id="add-account" method="POST" action="/accounts">
        <input type="text" name="account_name" placeholder="Account Name"/>
        <input type="submit" value="Add"/>
    </form>
    <h2>Accounts</h2>
    {% for account in accounts %}
        <h4 style="padding:.1em 0 0 2em;margin:.5em"><a href="/accounts/{{ '_'.join(account[0].split(' '))|lower}}">{{ account[0] }}</a></h4>
    {% endfor %}

{% else %}<br>
    <h2>{{ account[0] }} | {{ account[1]['id'] }}</h2>
    {% for k, v in account[1].items() %}
        {% if k == 'contact' %}
            <span style="padding:0 0 0 2em;text-decoration:underline">{{ k|title }}</span><br>
            {% for name, detail in v.items() %}
                {% if name in ('website', 'phone') %}
                    {% if detail is mapping %}
                        <span style="padding:0 0 0 4em;text-decoration:underline">{{ name|title }}</span><br>
                        {% for subname, subdetail in detail.items() %}
                            {% if name == 'website' %}
                                <span style="padding:0 0 0 6em"><span style="text-decoration:underline">{{ subname|title }}</span>: <a href="{{ subdetail }}" target="_blank">{{ subdetail }}</a></span><br>
                            {% elif name == 'phone' %}
                                <span style="padding:0 0 0 6em"><span style="text-decoration:underline">{{ subname|title }}</span>: <a href="tel:{{ subdetail }}" target="_blank">{{ subdetail }}</a></span><br>
                            {% endif %}
                        {% endfor %}
                    {% else %}
                        {% if name == 'website' %}
                            <span style="padding:0 0 0 4em;text-decoration:underline">{{ name|title }}</span>: <a href="{{ detail }}" target="_blank">{{ detail }}</a><br>
                        {% elif name == 'phone' %}
                            <span style="padding:0 0 0 4em;text-decoration:underline">{{ name|title }}</span>: <a href="tel:{{ detail }}" target="_blank">{{ detail }}</a><br>
                        {% endif %}
                    {% endif %}
                {% else %}
                    <span style="padding:0 0 0 4em"><span style="text-decoration:underline">{{ name|title }}</span>: {{ detail }}</span><br>
                {% endif %}
            {% endfor %}
        {% elif k != 'id' %}
            {% if k == 'website' %}
                <span style="padding:0 0 0 2em"><span style="text-decoration:underline">{{ k|title }}</span>: <a href="{{ v }}" target="_blank">{{ v }}</a></span><br>
            {% else %}
                <span style="padding:0 0 0 2em"><span style="text-decoration:underline">{{ k|title }}</span>: {{ v }}</span>
            {% endif %}            
        {% endif %}
    {% endfor %}
{% endif %}
