// install (please make sure versions match peerDependencies)
// yarn add @nivo/core @nivo/bar
import React from 'react';
import { ResponsiveBar } from '@nivo/bar';
import { useAppConfig } from '@eeacms/search';
import { encodeFilters } from './utils';
// make sure parent container have a defined height when using
// responsive component, otherwise height will be 0 and
// no chart will be rendered.
// website examples showcase many properties,
// you'll often use just a few of them.

export const BarChart = ({
  data /* see data tab */,
  keys,
  indexBy = 'country',
  fieldX,
  fieldY,
}) => {
  let searchOnClick = false;
  if (fieldX !== undefined && fieldY !== undefined) {
    searchOnClick = true;
  }
  const { appConfig } = useAppConfig();

  return (
    <ResponsiveBar
      data={data}
      keys={keys}
      indexBy={indexBy}
      margin={{ top: 50, right: 200, bottom: 50, left: 60 }}
      padding={0.3}
      valueScale={{ type: 'linear' }}
      indexScale={{ type: 'band', round: true }}
      valueFormat={{ format: '', enabled: false }}
      colors={{ scheme: 'nivo' }}
      onClick={(node, event) => {
        if (searchOnClick) {
          const getUrl = window.location;
          const baseUrl = getUrl.href.split('/').slice(0, -1).join('/');
          const newUrl =
            baseUrl +
            appConfig.wiseSearchPath +
            encodeFilters([
              [fieldX, node.data.Descriptor, 'any'],
              [fieldY, node.id, 'any'],
            ]);
          window.location.replace(newUrl);
        } else {
        }
      }}
      defs={[
        {
          id: 'dots',
          type: 'patternDots',
          background: 'inherit',
          color: '#38bcb2',
          size: 4,
          padding: 1,
          stagger: true,
        },
        {
          id: 'lines',
          type: 'patternLines',
          background: 'inherit',
          color: '#eed312',
          rotation: -45,
          lineWidth: 6,
          spacing: 10,
        },
      ]}
      fill={[]}
      borderColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
      axisTop={null}
      axisRight={null}
      axisBottom={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        // legend: 'country',
        legendPosition: 'middle',
        legendOffset: 32,
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        // legend: 'Count',
        legendPosition: 'middle',
        legendOffset: -40,
      }}
      labelSkipWidth={12}
      labelSkipHeight={12}
      labelTextColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
      legends={[
        {
          dataFrom: 'keys',
          anchor: 'bottom-right',
          direction: 'column',
          justify: false,
          translateX: 200,
          translateY: 0,
          itemsSpacing: 2,
          itemWidth: 180,
          itemHeight: 20,
          itemDirection: 'left-to-right',
          itemOpacity: 0.85,
          symbolSize: 20,
          effects: [
            {
              on: 'hover',
              style: {
                itemOpacity: 1,
              },
            },
          ],
        },
      ]}
    />
  );
};
