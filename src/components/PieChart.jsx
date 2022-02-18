import React from 'react';
import { ResponsivePie } from '@nivo/pie';
import { useSearchContext } from '@eeacms/search/lib/hocs';
import { openFacetsAtom } from '@eeacms/search/components/Facets/state';
import { useAtom } from 'jotai';
import { useUpdateAtom } from 'jotai/utils';
import { useAppConfig } from '@eeacms/search';

export const PieChart = ({ data, field, ...rest }) => {
  const searchContext = useSearchContext();
  const { addFilter } = searchContext;

  let searchOnClick = false;
  if (field !== undefined) {
    searchOnClick = true;
  }

  const [openFacets] = useAtom(openFacetsAtom);
  const updateOpenFacets = useUpdateAtom(openFacetsAtom);
  const { appConfig } = useAppConfig();

  return (
    <ResponsivePie
      field={field}
      data={data}
      margin={{ top: -80, right: 40, bottom: 90, left: 40 }}
      innerRadius={0.5}
      padAngle={0.7}
      cornerRadius={3}
      activeOuterRadiusOffset={8}
      borderWidth={1}
      enableArcLinkLabels={false}
      borderColor={{ from: 'color', modifiers: [['darker', 0.2]] }}
      arcLinkLabelsSkipAngle={10}
      arcLinkLabelsTextColor="#333333"
      arcLinkLabelsThickness={2}
      arcLinkLabelsColor={{ from: 'color' }}
      arcLabelsSkipAngle={10}
      arcLabelsTextColor={{ from: 'color', modifiers: [['darker', 2]] }}
      fill={[]}
      onClick={(node, event) => {
        if (searchOnClick) {
          const getUrl = window.location;
          const baseUrl = getUrl.protocol + '//' + getUrl.host;
          window.location.replace(baseUrl + appConfig.wiseSearchPath);
          // let temp = openFacets;
          // temp[field] = { opened: true };
          // updateOpenFacets(temp);
          // addFilter(field, node.id, 'any');
        } else {
          // console.log('Unknown field.');
        }
      }}
      legends={[
        {
          anchor: 'top',
          direction: 'column',
          justify: false,
          translateX: -30,
          translateY: 440,
          itemWidth: 100,
          itemHeight: 20,
          itemsSpacing: 0,
          symbolSize: 10,
          itemDirection: 'left-to-right',
        },
      ]}
      {...rest}
    />
  );
};
