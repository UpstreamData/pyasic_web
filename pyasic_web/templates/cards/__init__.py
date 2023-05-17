# ------------------------------------------------------------------------------
#  Copyright 2022 Upstream Data Inc                                            -
#                                                                              -
#  Licensed under the Apache License, Version 2.0 (the "License");             -
#  you may not use this file except in compliance with the License.            -
#  You may obtain a copy of the License at                                     -
#                                                                              -
#      http://www.apache.org/licenses/LICENSE-2.0                              -
#                                                                              -
#  Unless required by applicable law or agreed to in writing, software         -
#  distributed under the License is distributed on an "AS IS" BASIS,           -
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    -
#  See the License for the specific language governing permissions and         -
#  limitations under the License.                                              -
# ------------------------------------------------------------------------------
from abc import ABC, abstractmethod
from typing import List, Optional, Type

import jinja2
from pydantic import BaseModel


class CardModifier(BaseModel):
    title: str
    name: str


GRAPH_MODIFIER = CardModifier(title="Graph", name="graph")


class HTMLCard(ABC):
    def __init__(self, title: str, name: str, data_endpoint: str):
        self.title = title
        self.name = name
        self.data_endpoint = data_endpoint
        self.modifier: Optional[CardModifier] = None

    @abstractmethod
    def generate_js(self) -> jinja2.Template:
        pass

    @abstractmethod
    def generate_html(self) -> jinja2.Template:
        pass


class BasicCard(HTMLCard):
    def generate_js(self):
        data = f"""
        function update_{self.name}_card(data) {{
            {self.name}_card = document.getElementById("{self.name}_card");
            if (!(data.hasOwnProperty("data") && Object.keys(data["data"]).length > 0 && !!{self.name}_card)) {{
                return;
            }}
            var unit = data["data"][Object.keys(data["data"])[0]]["unit"]
            const miner_data = data["data"]
            if (data["combine_method"] == "sum") {{
                var sum = Object.values(miner_data).reduce((acc, curr) => acc + curr.value, 0);
                var total = +sum.toFixed(2)
            }} else if (data["combine_method"] == "avg") {{
                var sum = Object.values(miner_data).reduce((acc, curr) => acc + curr.value, 0);
                var avg = sum / Object.keys(miner_data).length
                var total = +avg.toFixed(2)
            }} else {{
                var total = miner_data[Object.keys(data["data"])[0]]["value"];
            }}
            if (unit == "") {{
                {self.name}_card.innerHTML = total
            }} else {{
                {self.name}_card.innerHTML = total + " " + unit
            }}
        }}
        """
        return jinja2.Template(data)

    def generate_html(self):
        data = f"""
        <div class="col col-xs-6 col-sm-4 col-md-3 my-2">
            <div class="card text-center">
                <div class="card-header fw-bold">{ self.title }</div>
                <div class="card-body hashrate-header d-flex align-items-center h4 p-0 m-0">
                    <div class="mx-auto fw-bolder" id="{ self.name }_card"></div>
                </div>
            </div>
        </div>
        """
        return jinja2.Template(data)

class BooleanCard(HTMLCard):
    def generate_js(self):
        data = f"""
        function update_{self.name}_card(data) {{
            {self.name}_card = document.getElementById("{self.name}_card");
            if (!(data.hasOwnProperty("data") && Object.keys(data["data"]).length > 0 && !!{self.name}_card)) {{
                return;
            }}
            var unit = data["data"][Object.keys(data["data"])[0]]["unit"]
            const miner_data = data["data"]
            var val = miner_data[Object.keys(data["data"])[0]]["value"];
            if (val == 1) {{
                {self.name}_card.innerHTML = "<b class='fs-1'>✓</b>"
            }} else {{
                {self.name}_card.innerHTML = "<b class='fs-1'>✗</b>"
            }}
        }}
        """
        return jinja2.Template(data)

    def generate_html(self):
        data = f"""
        <div class="col col-xs-6 col-sm-4 col-md-3 my-2">
            <div class="card text-center">
                <div class="card-header fw-bold">{ self.title }</div>
                <div class="card-body hashrate-header d-flex align-items-center h4 p-0 m-0">
                    <div class="mx-auto fw-bolder" id="{ self.name }_card"></div>
                </div>
            </div>
        </div>
        """
        return jinja2.Template(data)


class GraphCard(HTMLCard):
    def __init__(self, title: str, name: str, data_endpoint: str):
        super().__init__(title, name, data_endpoint)
        self.modifier: Optional[CardModifier] = GRAPH_MODIFIER

    def generate_html(self):
        data = f"""
        <div class="col col-12 col-sm-6 my-2">
            <div class="card">
                <div class="card-header fw-bold text-center">{self.title}</div>
                <div class="card-body">
                    <canvas id="{self.name}-{self.modifier.name}_card" class="w-100 h-100" style="max-height:187.5px;"></canvas>
                </div>
            </div>
        </div>
        """
        return jinja2.Template(data)

    def generate_js(self):
        data = f"""
        const {self.name}_{self.modifier.name}_ctx = document.getElementById('{self.name}-{self.modifier.name}_card').getContext('2d');
        const {self.name}_{self.modifier.name}_gradient = {self.name}_{self.modifier.name}_ctx.createLinearGradient(0, 0, {self.name}_{self.modifier.name}_ctx.canvas.width, 0);
        {self.name}_{self.modifier.name}_gradient.addColorStop(0, '#D0368A');
        {self.name}_{self.modifier.name}_gradient.addColorStop(0.99, '#708AD4');
        const {self.name}_{self.modifier.name}_chart = new Chart({self.name}_{self.modifier.name}_ctx, {{
            type: 'line', 
            data: {{
                datasets: [{{
                    label: '{self.title}', data: [], 
                    borderColor: function(context) {{
                        const {self.name}_{self.modifier.name}_ctx_chart = context.chart;
                        const {{ctx, chartArea}} = {self.name}_{self.modifier.name}_ctx_chart;
                        if (!chartArea) {{
                            return;
                        }}
                        return getGradient(ctx, chartArea);
                    }},
                    borderWidth: 4, pointRadius: 2, fill: true
                }}]
            }}, 
            options: {{
                animation: false, plugins: {{legend: {{display: false}}}},
                responsive: true, 
                scales: {{
                    x: {{type: 'time', time: {{unit: 'minute', max: 30}}}}, 
                    y: {{type: 'linear', min: 0, ticks: {{callback: function(value, index, values) {{return value;}}}}}}
                }}
            }}
        }});

        function update_{self.name}_{self.modifier.name}_card(data) {{
            if (!(data.hasOwnProperty("data") && Object.keys(data["data"]).length > 0 && !!{self.name}_card)) {{
                return;
            }}
            var unit = data["data"][Object.keys(data["data"])[0]]["unit"]
            const miner_data = data["data"]
            if (data["combine_method"] == "sum") {{
                var sum = Object.values(miner_data).reduce((acc, curr) => acc + curr.value, 0);
                var total = +sum.toFixed(2)
            }} else if (data["combine_method"] == "avg") {{
                var sum = Object.values(miner_data).reduce((acc, curr) => acc + curr.value, 0);
                var avg = sum / Object.keys(miner_data).length
                var total = +avg.toFixed(2)
            }}
            {self.name}_{self.modifier.name}_chart.data.datasets[0].data.push({{ x: new Date(), y: total }});
            {self.name}_{self.modifier.name}_chart.options.scales.y.ticks.callback = function(value, index, values) {{
                return value + ' ' + unit;
            }};
        
            // Remove older data points if number of data points exceeds 30
            if ({self.name}_{self.modifier.name}_chart.data.datasets[0].data.length > 30) {{
                {self.name}_{self.modifier.name}_chart.data.datasets[0].data.splice(0, 1);
            }}
        
            {self.name}_{self.modifier.name}_chart.update();
        }}"""
        return jinja2.Template(data)


class CountCard(BasicCard):
    def generate_js(self) -> jinja2.Template:
        data = f'''
        function update_{self.name}_card(data) {{
            {self.name}_card = document.getElementById("{self.name}_card");
            if (!(data.hasOwnProperty("value") && data.hasOwnProperty("unit") || !!{self.name}_card)) {{
                return;
            }}
            var unit = data["unit"]
            var val = data["value"]
            if (unit == "") {{
                {self.name}_card.innerHTML = val
            }} else {{
                {self.name}_card.innerHTML = val + " " + unit
            }}
        }}
        '''
        return jinja2.Template(data)


class PoolsCard(HTMLCard):
    def generate_html(self) -> jinja2.Template:
        data = f'''
        <div class="col col-12 col-sm-6 my-2">
            <div class="card">
                <div class="card-header fw-bold text-center">{self.title}</div>
                <div class="card-body">
                    <div style="height: 187.5px;
                                overflow-y:scroll"
                         class="p-0 thick-fancy-scroll list-group pe-3"
                         id="{self.name}_card"></div>
                </div>
            </div>
        </div>
        '''
        return jinja2.Template(data)

    def generate_js(self) -> jinja2.Template:
        data = f'''
        function update_{self.name}_card(data) {{
            {self.name}_card = document.getElementById("{self.name}_card");
            if (!(data.hasOwnProperty("data") && Object.keys(data["data"]).length > 0 && !!{self.name}_card)) {{
                return;
            }}
            {self.name}_card.innerHTML = ""
            poolUsers = {{}};
            for (const item of Object.values(data["data"])) {{
                poolUsers[item["value"]] = poolUsers.hasOwnProperty(item["value"]) ? poolUsers[item["value"]] + 1 : 1;
            }}
            for (item in poolUsers) {{
                pools_card.innerHTML += `<div class ="list-group-item d-flex justify-content-between">${{item}}<span class="badge bg-fancy-gradient rounded-pill align-items-middle p-2 m-0" style="width:50px;">${{poolUsers[item]}}</span></div>`
            }}
        }}
        '''
        return jinja2.Template(data)


class ErrorsCard(HTMLCard):
    def generate_html(self) -> jinja2.Template:
        data = f'''
        <div class="col col-12 col-sm-6 my-2">
            <div class="card">
                <div class="card-header fw-bold text-center">{self.title}</div>
                <div class="card-body">
                    <div style="height: 187.5px;
                                overflow-y:scroll"
                         class="p-0 thick-fancy-scroll list-group pe-3"
                         id="{self.name}_card"></div>
                </div>
            </div>
        </div>
        '''
        return jinja2.Template(data)

    def generate_js(self) -> jinja2.Template:
        data = f"""
        function update_{self.name}_card(data) {{
            {self.name}_card = document.getElementById("{self.name}_card");
            if (!(data.hasOwnProperty("data") && Object.keys(data["data"]).length > 0 && !!{self.name}_card)) {{
                return;
            }}
            let errorsHtml = "";
            
            for (const ip of Object.keys(data.data)) {{
                const errors = data.data[ip].value;
                if (errors.length > 0) {{
                    const minerId = ip.replaceAll(".", "-");
                    const errorsElem = document.getElementById(`errors_${{minerId}}`);
                    const showClass = errorsElem && errorsElem.classList.contains("show") ? "show" : "";
            
                    let minerErrorsHtml = `
                    <a
                    data-bs-toggle="collapse"
                    href="#errors_${{minerId}}"
                    role="button"
                    class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error ${{showClass}}"
                    aria-expanded="${{showClass ? 'true' : 'false'}}"
                    >
                    ${{ip}}
                    <span class="badge bg-fancy-gradient rounded-pill align-items-middle p-2 m-0" style="width:50px;">
                    ${{errors.length}}
                    </span>
                    </a>
                    <div class="collapse no-transition multi-collapse my-0 py-0 ms-5 ${{showClass}}" id="errors_${{minerId}}">
                    `;
            
                    for (const error of errors) {{
                        minerErrorsHtml += `
                        <div class="list-group-item no-transition miner-error-item">${{error.error_message}}</div>
                        `;
                    }}
            
                    minerErrorsHtml += "</div>";
                    errorsHtml += minerErrorsHtml;
                }}
            }}
            {self.name}_card.innerHTML = errorsHtml;
        }}
        """
        return jinja2.Template(data)


class LightsCard(HTMLCard):
    def generate_html(self) -> jinja2.Template:
        data = '''
        <div class="col col-12 col-sm-6 my-2">
            <div class="card-group">
                <div class="card">
                    <div class="card-header fw-bold">Lights On</div>
                    <div class="card-body">
                        <div style="height: 187.5px;
                                    overflow-y:scroll"
                             class="p-0 thick-fancy-scroll list-group pe-3"
                             id="lights_on_card"></div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header fw-bold">Lights Off</div>
                    <div class="card-body">
                        <div style="height: 187.5px;;
                                    overflow-y:scroll"
                             class="p-0 thick-fancy-scroll list-group pe-3"
                             id="lights_off_card"></div>
                    </div>
                </div>
            </div>
        </div>
        '''
        return jinja2.Template(data)

    def generate_js(self) -> jinja2.Template:
        data = f'''
        function update_{self.name}_card(data) {{
            {self.name}_on_card = document.getElementById("{self.name}_on_card");
            {self.name}_off_card = document.getElementById("{self.name}_off_card");
            if (!(data.hasOwnProperty("data") && Object.keys(data["data"]).length > 0 && !!{self.name}_on_card && !!{self.name}_off_card)) {{
                return;
            }}
            lights_on_card.innerHTML = ""
            lights_off_card.innerHTML = ""
            for (const ip of Object.keys(data["data"])) {{
                if (data["data"][ip]) {{
                    lights_on_card.innerHTML += '<div class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + ip + '</div>'
                }} else {{
                    lights_off_card.innerHTML += '<div class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + ip + '</div>'
                }}
            }}
        }}
        '''
        return jinja2.Template(data)



class AvailableCards:
    def __init__(self, cards: List[HTMLCard], modifiers: List[CardModifier]):
        self.cards = cards
        self.modifiers = modifiers


    def get_modifier(self, modifier_name: str):
        for instance in self.modifiers:
            if instance.name == modifier_name:
                return instance

    def get_card(self, card_name: str):
        split_name = card_name.split("-")
        mod = split_name[1] if len(split_name) > 1 else ""
        name = split_name[0]
        for instance in self.cards:
            if instance.name == name:
                if instance.modifier == self.get_modifier(mod):
                    return instance
