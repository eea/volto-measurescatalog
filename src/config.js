import { suiFacet } from '@eeacms/search';
import WiseLayout from './components/WiseLayout';
import WiseLayoutCharts from './components/WiseLayoutCharts';
import ChartsIntro from './components/ChartsIntro';
import ListingViewItem from './components/ListingViewItem';
import { ResultModelExtended } from './models';

const details = {
  titleField: 'Measure name',
  extraFields: [
    {
      field: 'Origin of the measure',
      label: 'Origin of the measure',
    },
    {
      field: 'Descriptors',
      label: 'MSFD Descriptors',
    },
    {
      field: 'Sector',
      label: 'Sector',
    },
  ],
  sections: [
    {
      fields: [
        { field: 'Measure name' },
        { field: 'Sector' },
        { field: 'Use or activity' },
        { field: 'Origin of the measure' },
        { field: 'Nature of the measure' },
        { field: 'Status' },
        {
          field: 'Measure Impacts to',
          label: 'Measure impacts to',
        },
        {
          field: 'Measure Impacts to (further details)',
          label: 'Measure impacts to, further details ',
        },
        { field: 'Water body category' },
        { field: 'Spatial scope' },
        { field: 'Country', label: 'Country coverage' },
      ],
    },
    {
      title: 'Further information',
      condition: (rec) =>
        rec['Origin of the measure']?.raw === 'WFD (Directive 2000/60/EC)',
      fields: [
        { field: 'Nature of physical modification' },
        { field: 'Effect on hydromorphology' },
        { field: 'Ecological impacts' },
      ],
    },
    {
      title: 'Further information',
      condition: (rec) =>
        rec['Origin of the measure']?.raw === 'MSFD (Directive 2008/56/EC)',
      fields: [
        { field: 'Link to existing policies' },
        { field: 'KTMs it links to' },
        { field: 'Relevant targets' },
        { field: 'Relevant features from MSFD Annex III' },
        { field: 'Spatial  scope_MSFD', label: 'MSFD Spatial scope' },
        { field: 'Keywords' },
      ],
    },
    {
      title: 'Further information',
      condition: (rec) => {
        return (
          rec['Origin of the measure']?.raw === 'HD (Directive 92/43/EEC)' &&
          rec['MeasureCode'] &&
          rec['MeasureCode'].raw.startsWith('HDH')
        );
      },
      fields: [
        { field: 'Measure purpose' },
        { field: 'Measure type recommended to address E02 and/or E03' },
        { field: 'Measure location' },
        { field: 'Measure response' },
        { field: 'Measure additional info' },
        { field: 'Pressure type', label: 'Type of pressure' },
        { field: 'Pressure name' },
        { field: 'Ranking' },
        { field: 'Region' },
      ],
    },
    {
      title: 'Further information',
      condition: (rec) => {
        return (
          rec['Origin of the measure']?.raw === 'HD (Directive 92/43/EEC)' &&
          rec['MeasureCode'] &&
          rec['MeasureCode'].raw.startsWith('HDSP')
        );
      },
      fields: [
        { field: 'Measure purpose' },
        { field: 'Measure type recommended to address E02 and/or E03' },
        { field: 'Measure location' },
        { field: 'Measure response' },
        { field: 'Measure additional info' },
        { field: 'Pressure type', label: 'Type of pressure' },
        { field: 'Pressure name' },
        { field: 'Ranking' },
        { field: 'Region', label: 'Marine region' },
      ],
    },
    {
      title: 'Further information',
      condition: (rec) =>
        rec['Origin of the measure']?.raw === 'BD (Directive 79/409/EEC)',
      fields: [
        { field: 'Measure purpose' },
        { field: 'Measure type recommended to address E02 and/or E03' },
        { field: 'Measure location' },
        { field: 'Measure response' },
        { field: 'Measure additional info' },
        { field: 'Pressure type', label: 'Type of pressure' },
        { field: 'Pressure name' },
        { field: 'Ranking' },
        { field: 'Season' },
      ],
    },
    {
      title: 'Further information',
      condition: (rec) =>
        rec['Origin of the measure']?.raw === 'MSPD (Directive 2008/56/EC)',
      fields: [
        { field: 'Nature of physical modification' },
        { field: 'MSPD implementation status' },
        { field: 'Shipping Tackled' },
        { field: 'Traffic separation scheme' },
        { field: 'Priority Areas' },
        { field: 'Approaching Areas' },
        { field: 'Precautionary areas' },
        { field: 'Areas to be avoided' },
        { field: 'Future Scenarios' },
        { field: 'Source' },
        { field: 'Keywords' },
        { field: 'Authority' },
        { field: 'General View' },
        { field: 'Ports' },
        { field: 'Future Expectations' },
        { field: 'Safety manner' },
        { field: 'Objective' },
        { field: 'Categories' },
      ],
    },
    {
      title: 'Further information',
      condition: (rec) => rec['Origin of the measure']?.raw === 'Sectorial',
      fields: [
        { field: 'Impacts' },
        { field: 'Spatial scale' },
        { field: 'Source', label: 'Source(s)' },
      ],
    },
  ],
};

export const wise_minimal_config = {
  // host: 'http://localhost:7000',
  title: 'Catalogue of Measures',
  titleIsLink: true,
  elastic_index: 'wise_catalogue_measures',
  enableNLP: false,
  layoutComponent: 'WiseLayoutCharts',
  facetsListComponent: 'DefaultFacetsList',
  searchBoxInputComponent: 'SimpleSearchInput',
  wiseSearchPath: '/catalogue',

  permanentFilters: [],
  facets: [],
  highlight: {
    queryParams: {
      fragment_size: 200,
      number_of_fragments: 3,
    },
    fields: ['description'],
    queryBuilder: {
      factory: 'highlightQueryBuilder',
    },
  },

  sortOptions: [
    {
      name: 'Title',
      value: 'Measure name',
      direction: 'asc',
    },
  ],

  initialView: {
    factory: 'ChartsIntro',
  },

  tableViewParams: {},
  listingViewParams: {},

  download_fields: [],

  resultItemModel: {
    factory: 'ResultModelExtended',
  },
};

export const wise_config = {
  // host: 'http://localhost:7000',
  title: 'Catalogue of Measures',
  titleIsLink: true,
  elastic_index: 'wise_catalogue_measures',
  enableNLP: false,
  layoutComponent: 'WiseLayout',
  facetsListComponent: 'DefaultFacetsList',
  searchBoxInputComponent: 'SimpleSearchInput',
  useSearchPhrases: false,
  searchAsYouType: false,
  searchInputPlaceholder: 'What are you looking for?',
  landingPageURL: 'charts',

  permanentFilters: [],

  facets: [
    suiFacet({
      field: 'Measure Impacts to',
      label: 'Measure impacts to',
      isMulti: true,
      isFilterable: false,
      show: 100,
      factory: 'MultiTermFacet',
      wrapper: 'AccordionFacetWrapper',
    }),
    suiFacet({
      field: 'Origin of the measure',
      label: 'Origin of the measure',
      isMulti: true,
      isFilterable: false,
      show: 100,
      factory: 'MultiTermFacet',
      wrapper: 'AccordionFacetWrapper',
    }),
    suiFacet({
      field: 'Sector',
      isMulti: true,
      isFilterable: false,
      show: 100,
      factory: 'MultiTermFacet',
      wrapper: 'AccordionFacetWrapper',
    }),
    suiFacet({
      field: 'Descriptors',
      label: 'MSFD Descriptors',
      isMulti: true,
      isFilterable: false,
      show: 100,
      factory: 'MultiTermFacet',
      wrapper: 'AccordionFacetWrapper',
      facetValues: [
        {
          value: 'D1',
          name: 'D1. Biodiversity',
          url:
            'https://ec.europa.eu/environment/marine/good-environmental-status/descriptor-1/index_en.htm',
        },
        {
          value: 'D2',
          name: 'D2. Non-indigenous Species',
          url:
            'https://ec.europa.eu/environment/marine/good-environmental-status/descriptor-2/index_en.htm',
        },
        {
          value: 'D3',
          name: 'D3.  Commercial Fish and shellfish',
          url:
            'https://ec.europa.eu/environment/marine/good-environmental-status/descriptor-3/index_en.htm',
        },
        {
          value: 'D4',
          name: 'D4. Food Webs',
          url:
            'https://ec.europa.eu/environment/marine/good-environmental-status/descriptor-4/index_en.htm',
        },
        {
          value: 'D5',
          name: 'D5. Eutrophication',
          url:
            'https://ec.europa.eu/environment/marine/good-environmental-status/descriptor-5/index_en.htm',
        },
        {
          value: 'D6',
          name: 'D6. Sea-floor Integrity',
          url:
            'https://ec.europa.eu/environment/marine/good-environmental-status/descriptor-6/index_en.htm',
        },
        {
          value: 'D7',
          name: 'D7. Hydrographical Conditions',
          url:
            'https://ec.europa.eu/environment/marine/good-environmental-status/descriptor-7/index_en.htm',
        },
        {
          value: 'D8',
          name: 'D8. Contaminants',
          url:
            'https://ec.europa.eu/environment/marine/good-environmental-status/descriptor-8/index_en.htm',
        },
        {
          value: 'D9',
          name: 'D9. Contaminants in Seafood',
          url:
            'https://ec.europa.eu/environment/marine/good-environmental-status/descriptor-9/index_en.htm',
        },
        {
          value: 'D10',
          name: 'D10. Marine Litter',
          url:
            'https://ec.europa.eu/environment/marine/good-environmental-status/descriptor-10/index_en.htm',
        },
        {
          value: 'D11',
          name: 'D11. Energy including Underwater Noise',
          url:
            'https://ec.europa.eu/environment/marine/good-environmental-status/descriptor-11/index_en.htm',
        },
      ],
    }),
    suiFacet({
      field: 'Country',
      isMulti: true,
      isFilterable: false,
      show: 100,
      factory: 'MultiTermFacet',
      wrapper: 'AccordionFacetWrapper',
    }),
  ],
  highlight: {
    queryParams: {
      fragment_size: 200,
      number_of_fragments: 3,
    },
    fields: ['description'],
    queryBuilder: {
      factory: 'highlightQueryBuilder',
    },
  },

  sortOptions: [
    {
      name: 'Title',
      value: 'Measure name',
      direction: 'asc',
    },
  ],
  tableViewParams: {
    titleField: 'Measure name',
    columns: [
      {
        title: 'Measure name',
        field: 'Measure name',
      },
      {
        title: 'Code',
        field: 'id',
      },
      {
        title: 'Origin of the measure',
        field: 'Origin of the measure',
      },
      {
        field: 'Descriptors',
        label: 'MSFD Descriptors',
      },
      {
        field: 'Sector',
        label: 'Sector',
      },
    ],
    details,
  },
  listingViewParams: {
    titleField: 'Measure name',
    // urlField: 'CodeCatalogue',
    extraFields: [
      {
        field: 'Origin of the measure',
        label: 'Origin of the measure',
      },
      {
        field: 'Descriptors',
        label: 'MSFD Descriptors',
      },
      {
        field: 'Sector',
        label: 'Sector',
      },
    ],
    details,
  },

  download_fields: [
    {
      field: 'Measure name',
      name: 'Measure name',
    },
    {
      field: 'Origin of the measure',
      name: 'Origin of the measure',
    },
    {
      field: 'Descriptors',
      name: 'MSFD Descriptors',
    },
    {
      field: 'Sector',
      name: 'Sector',
    },
  ],

  resultItemModel: {
    factory: 'ResultModelExtended',
  },

  vocab: {
    Descriptors: {
      D1: 'D1. Biodiversity',
      D2: 'D2. Non-indigenous Species',
      D3: 'D3.  Commercial Fish and shellfish',
      D4: 'D4. Food Webs',
      D5: 'D5. Eutrophication',
      D6: 'D6. Sea-floor Integrity',
      D7: 'D7. Hydrographical Conditions',
      D8: 'D8. Contaminants',
      D9: 'D9. Contaminants in Seafood',
      D10: 'D10. Marine Litter',
      D11: 'D11. Energy including Underwater Noise',
    },
  },
};

export const wise_resolve = {
  WiseLayout: {
    component: WiseLayout,
  },
  WiseLayoutCharts: {
    component: WiseLayoutCharts,
  },
  ChartsIntro: {
    component: ChartsIntro,
  },
  ListingViewItem: {
    component: ListingViewItem,
  },
  ResultModelExtended,
};
