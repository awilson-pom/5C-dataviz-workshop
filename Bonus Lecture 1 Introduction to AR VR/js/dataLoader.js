// Base DataLoader class
class DataLoader {
    constructor(containerId) {
        this.container = d3.select(`#${containerId}`);
        this.data = null;
        this.error = null;
        this.isLoading = false;
    }

    // Abstract method for loading data
    async loadData() {
        throw new Error('loadData method must be implemented');
    }

    // Show loading indicator
    showLoading() {
        this.isLoading = true;
        this.container.html('');
        this.container
            .append('div')
            .attr('class', 'loading')
            .text('Loading data...');
    }

    // Show error message
    showError(error) {
        this.error = error;
        this.container.html('');
        this.container
            .append('div')
            .attr('class', 'error')
            .text(`Error loading data: ${error.message}`);
    }

    // Clear the container
    clear() {
        this.container.html('');
    }
}

// JSONDataLoader class for loading JSON data
class JSONDataLoader extends DataLoader {
    constructor(containerId, url) {
        super(containerId);
        this.url = url;
    }

    async loadData() {
        try {
            this.showLoading();
            this.data = await d3.json(this.url);
            this.isLoading = false;
            return this.data;
        } catch (error) {
            this.showError(error);
            throw error;
        }
    }
}

// CSVDataLoader class for loading CSV data
class CSVDataLoader extends DataLoader {
    constructor(containerId, url) {
        super(containerId);
        this.url = url;
    }

    async loadData() {
        try {
            this.showLoading();
            this.data = await d3.csv(this.url);
            this.isLoading = false;
            return this.data;
        } catch (error) {
            this.showError(error);
            throw error;
        }
    }
}

// MultiDataLoader class for loading multiple data sources
class MultiDataLoader extends DataLoader {
    constructor(containerId, sources) {
        super(containerId);
        this.sources = sources; // Array of {url, type} objects
    }

    async loadData() {
        try {
            this.showLoading();
            const promises = this.sources.map(source => {
                switch(source.type.toLowerCase()) {
                    case 'json':
                        return d3.json(source.url);
                    case 'csv':
                        return d3.csv(source.url);
                    default:
                        throw new Error(`Unsupported data type: ${source.type}`);
                }
            });

            this.data = await Promise.all(promises);
            this.isLoading = false;
            return this.data;
        } catch (error) {
            this.showError(error);
            throw error;
        }
    }
}

// Example usage:
// const jsonLoader = new JSONDataLoader('visualization', 'https://api.example.com/data.json');
// jsonLoader.loadData()
//     .then(data => {
//         // Process and visualize JSON data
//         console.log('JSON data loaded:', data);
//     })
//     .catch(error => console.error('Error:', error));

// const csvLoader = new CSVDataLoader('visualization', 'https://api.example.com/data.csv');
// csvLoader.loadData()
//     .then(data => {
//         // Process and visualize CSV data
//         console.log('CSV data loaded:', data);
//     })
//     .catch(error => console.error('Error:', error));

// const multiLoader = new MultiDataLoader('visualization', [
//     { url: 'https://api.example.com/data1.json', type: 'json' },
//     { url: 'https://api.example.com/data2.csv', type: 'csv' }
// ]);
// multiLoader.loadData()
//     .then(([jsonData, csvData]) => {
//         // Process and visualize multiple data sources
//         console.log('Multiple data sources loaded:', { jsonData, csvData });
//     })
//     .catch(error => console.error('Error:', error));