class CovidVisualization {
    constructor(containerId) {
        this.containerId = containerId;
        this.container = document.getElementById(containerId);
        
        if (!this.container) {
            throw new Error(`Container with id '${containerId}' not found`);
        }

        this.margin = { top: 40, right: 80, bottom: 60, left: 80 };
        this.width = 800 - this.margin.left - this.margin.right;
        this.height = 500 - this.margin.top - this.margin.bottom;
        
        this.selectElement = null;
        this.svgContainer = null;
        this.svg = null;
        
        // Initialize with the API URL
        this.loader = new JSONDataLoader(containerId, 
            'https://disease.sh/v3/covid-19/countries');
        
        this.initializeContainer();
        this.loadAndVisualizeData();
    }

    initializeContainer() {
        this.container.innerHTML = '';

        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'controls';
        controlsDiv.style.marginBottom = '10px';
        
        this.selectElement = document.createElement('select');
        this.selectElement.style.padding = '5px';
        this.selectElement.style.marginRight = '10px';
        
        const options = [
            { value: 'cases', text: 'Total Cases' },
            { value: 'deaths', text: 'Total Deaths' },
            { value: 'recovered', text: 'Total Recovered' },
            { value: 'active', text: 'Active Cases' },
            { value: 'critical', text: 'Critical Cases' },
            { value: 'tests', text: 'Total Tests' }
        ];
        
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.text;
            this.selectElement.appendChild(optionElement);
        });
        
        this.selectElement.addEventListener('change', () => this.updateVisualization());
        
        controlsDiv.appendChild(this.selectElement);
        this.container.appendChild(controlsDiv);
        
        this.svgContainer = document.createElement('div');
        this.svgContainer.className = 'svg-container';
        this.container.appendChild(this.svgContainer);
    }

    async loadAndVisualizeData() {
        try {
            this.container.innerHTML = '<div style="padding: 20px;">Loading data...</div>';
            const data = await this.loader.loadData();
            
            if (!data || data.length === 0) {
                throw new Error('No data received from API');
            }

            this.data = data;
            this.initializeContainer();
            this.updateVisualization();
        } catch (error) {
            console.error('Error loading data:', error);
            this.showError(`Error loading data: ${error.message}`);
        }
    }

    createSVG() {
        this.svgContainer.innerHTML = '';
        
        this.svg = d3.select(this.svgContainer)
            .append('svg')
            .attr('width', this.width + this.margin.left + this.margin.right)
            .attr('height', this.height + this.margin.top + this.margin.bottom)
            .append('g')
            .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
    }

    updateVisualization() {
        try {
            if (!this.selectElement) {
                throw new Error('Select element not initialized');
            }

            const selectedMetric = this.selectElement.value;
            const metricLabels = {
                cases: 'Total Cases',
                deaths: 'Total Deaths',
                recovered: 'Total Recovered',
                active: 'Active Cases',
                critical: 'Critical Cases',
                tests: 'Total Tests'
            };

            // Process data for top 10 countries by selected metric
            const processedData = this.data
                .filter(d => d[selectedMetric] != null && d[selectedMetric] > 0)
                .sort((a, b) => b[selectedMetric] - a[selectedMetric])
                .slice(0, 10)
                .map(d => ({
                    location: d.country,
                    value: d[selectedMetric],
                    flag: d.countryInfo.flag
                }));

            if (processedData.length === 0) {
                throw new Error('No valid data for selected metric');
            }

            this.createSVG();
            this.createVisualization(processedData, metricLabels[selectedMetric]);
        } catch (error) {
            console.error('Error updating visualization:', error);
            this.showError(`Error updating visualization: ${error.message}`);
        }
    }

    showError(message) {
        if (this.container) {
            this.container.innerHTML = `
                <div style="color: red; padding: 20px;">
                    ${message}<br>
                    Please check the console for more details.
                </div>
            `;
        }
    }

    createVisualization(data, metricLabel) {
        // Create scales
        const x = d3.scaleBand()
            .range([0, this.width])
            .padding(0.1)
            .domain(data.map(d => d.location));

        const y = d3.scaleLinear()
            .range([this.height, 0])
            .domain([0, d3.max(data, d => d.value)]);

        // Create color scale
        const colorScale = d3.scaleSequential()
            .domain([0, d3.max(data, d => d.value)])
            .interpolator(d3.interpolateBlues);

        // Add axes
        this.svg.append('g')
            .attr('transform', `translate(0,${this.height})`)
            .call(d3.axisBottom(x))
            .selectAll('text')
            .attr('transform', 'rotate(-45)')
            .style('text-anchor', 'end');

        this.svg.append('g')
            .call(d3.axisLeft(y)
                .tickFormat(d => d3.format(',.0f')(d)));

        // Add title
        this.svg.append('text')
            .attr('x', this.width / 2)
            .attr('y', -this.margin.top / 2)
            .attr('text-anchor', 'middle')
            .style('font-size', '16px')
            .text(`COVID-19 ${metricLabel} by Country (Top 10)`);

        // Add bars with transition
        const bars = this.svg.selectAll('.bar')
            .data(data)
            .enter()
            .append('rect')
            .attr('class', 'bar')
            .attr('x', d => x(d.location))
            .attr('width', x.bandwidth())
            .attr('y', this.height)
            .attr('height', 0)
            .attr('fill', d => colorScale(d.value));

        bars.transition()
            .duration(750)
            .attr('y', d => y(d.value))
            .attr('height', d => this.height - y(d.value));

        // Add value labels
        this.svg.selectAll('.label')
            .data(data)
            .enter()
            .append('text')
            .attr('class', 'label')
            .attr('x', d => x(d.location) + x.bandwidth() / 2)
            .attr('y', d => y(d.value) - 5)
            .attr('text-anchor', 'middle')
            .text(d => d3.format(',.0f')(d.value))
            .style('font-size', '12px')
            .style('opacity', 0)
            .transition()
            .duration(750)
            .style('opacity', 1);

        // Add tooltips with flags
        const tooltip = d3.select('body')
            .append('div')
            .attr('class', 'tooltip')
            .style('opacity', 0);

        bars.on('mouseover', (event, d) => {
            tooltip.transition()
                .duration(200)
                .style('opacity', .9);
            tooltip.html(`
                <img src="${d.flag}" style="width: 30px; height: auto; margin-right: 5px;">
                <strong>${d.location}</strong><br/>
                ${metricLabel}: ${d3.format(',.0f')(d.value)}
            `)
                .style('left', (event.pageX + 10) + 'px')
                .style('top', (event.pageY - 28) + 'px');
        })
        .on('mouseout', () => {
            tooltip.transition()
                .duration(500)
                .style('opacity', 0);
        });
    }
}

// Initialize visualization when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    try {
        const visualization = new CovidVisualization('visualization');
    } catch (error) {
        console.error('Error initializing visualization:', error);
        const container = document.getElementById('visualization');
        if (container) {
            container.innerHTML = `
                <div style="color: red; padding: 20px;">
                    Error initializing visualization: ${error.message}<br>
                    Please check the console for more details.
                </div>
            `;
        }
    }
});