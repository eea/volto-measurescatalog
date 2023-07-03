import { mergeConfig, registry } from '@eeacms/search';
import { wise_config, wise_minimal_config, wise_resolve } from './config';
import codeSVG from '@plone/volto/icons/code.svg';
import ChartsBlockView from './ChartsBlock/ChartsBlockView';
import ChartsBlockEdit from './ChartsBlock/ChartsBlockEdit';

const getClientProxyAddress = () => {
  const url = new URL(window.location);
  url.pathname = '';
  url.search = '';
  return url.toString();
};

export function installMeasuresCatalogue(config) {
  const pjson = require('../package.json');

  const registry = config.settings.searchlib;
  const envConfig = mergeConfig(wise_config, registry.searchui.default);
  registry.searchui.wise = envConfig;
  registry.resolve = mergeConfig(wise_resolve, registry.resolve);
  registry.searchui.wise.resultViews[0].icon = 'list';
  registry.searchui.wise.resultViews[1].icon = 'table';

  const envConfigMin = mergeConfig(
    wise_minimal_config,
    registry.searchui.default,
  );
  registry.searchui.wisemin = envConfigMin;
  registry.searchui.wisemin.resultViews[0].icon = 'list';
  registry.searchui.wisemin.resultViews[1].icon = 'table';

  // making it suitable for es middleware
  registry.searchui.wise.elastic_index = `_es/wise`;
  registry.searchui.wisemin.elastic_index = `_es/wise`;

  envConfig.app_name = pjson.name;
  envConfig.app_version = pjson.version;

  envConfigMin.app_name = pjson.name;
  envConfigMin.app_version = pjson.version;

  if (
    typeof window !== 'undefined'
    // && process.env.RAZZLE_USE_ES_PROXY === 'true'
  ) {
    registry.searchui.wise.host =
      process.env.RAZZLE_ES_PROXY_ADDR || getClientProxyAddress();
    registry.searchui.wisemin.host =
      process.env.RAZZLE_ES_PROXY_ADDR || getClientProxyAddress();
  }

  return config;
}

const applyConfig = (config) => {
  config.blocks.blocksConfig.wmcharts = {
    id: 'wmcharts',
    title: 'WISE Marine Charts',
    icon: codeSVG,
    group: 'common',
    view: ChartsBlockView,
    edit: ChartsBlockEdit,
    restricted: false,
    mostUsed: false,
    blockHasOwnFocusManagement: false,
    sidebarTab: 1,
    security: {
      addPermission: [],
      view: [],
    },
  };

  config.settings.wmcharts = registry;
  return config;
};

export default function install(config) {
  applyConfig(config);
  return config;
}
