import React from 'react';
import SearchBlockView from '@eeacms/volto-searchlib/SearchBlock/SearchBlockView';

const View = (props) => {
  const config = {
    appName: 'wisemin',
  };

  return <SearchBlockView data={config} />;
};

export default View;
