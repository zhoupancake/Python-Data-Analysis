from flask import Flask, render_template
import src.dataAnalysis.display as display
import json as JSON

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/min_max_speed_each_position')
def min_max_speed_each_position():
    return display.min_max_speed_each_position().to_json(orient='records')


@app.route('/min_max_health_each_position')
def min_max_health_each_position():
    return display.min_max_health_each_position().to_json(orient='records')


@app.route('/distribution_speed_each_position')
def distribution_speed_each_position():
    return JSON.dumps(display.distribution_speed_each_position(), indent=2)


@app.route('/distribution_health_each_position')
def distribution_health_each_position():
    print(JSON.dumps(display.distribution_health_each_position(), indent=2))
    return JSON.dumps(display.distribution_health_each_position(), indent=2)


@app.route('/type_count_each_position')
def type_count_each_position():
    return display.type_count_each_position().to_json(orient='records')


@app.route('/attack_range_count_each_position')
def attack_range_count_each_position():
    return display.attack_range_count_each_position().to_json(orient='records')


@app.route('/relation_PhysicalDefense_PhysicalDamageReduction')
def relation_PhysicalDefense_PhysicalDamageReduction():
    return display.relation_PhysicalDefense_PhysicalDamageReduction().to_json(orient='records')


@app.route('/relation_MaximumMana_ManaRegeneration')
def relation_MaximumMana_ManaRegeneration():
    return display.relation_MaximumMana_ManaRegeneration().to_json(orient='records')


if __name__ == '__main__':
    distribution_speed_each_position()
    app.run(debug=True)
