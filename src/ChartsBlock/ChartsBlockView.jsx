import React from 'react';
import ChartsIntro from './../components/ChartsIntro';
import SearchBlockView from '@eeacms/volto-searchlib/SearchBlock/SearchBlockView';

const View = (props) => {
  // return <ChartsIntro />;
  //
  // return <div>CHARTS VIEW</div>;
  const config = {
    appName: 'wisemin',
  };

  return <SearchBlockView data={config} />;
};

export default View;

/*
  TODO -------------------
  1. Import SearchBlockView                                            - OK
  2. Create alternative Layout: src/components/WiseLayoutTest.jsx      - OK
  3. Create a simplified config to be used by SearchBlockView for Home - OK ~?
  4. Include Charts in new Layout WIP                                  - OK ~?
*/
