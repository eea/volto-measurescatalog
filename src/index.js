import React from 'react';
import { mergeConfig } from '@eeacms/search';
import { wise_config, wise_resolve } from './config';

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

  // making it suitable for es middleware
  registry.searchui.wise.elastic_index = `_es/wise`;

  envConfig.app_name = pjson.name;
  envConfig.app_version = pjson.version;

  if (
    typeof window !== 'undefined'
    // && process.env.RAZZLE_USE_ES_PROXY === 'true'
  ) {
    registry.searchui.wise.host =
      process.env.RAZZLE_ES_PROXY_ADDR || getClientProxyAddress();
  }

  console.log('config', config.settings.searchlib);

  return config;
}

export default function install(config) {
  return config;
}
