import React from 'react';
import { Grid } from 'semantic-ui-react';
// import '../less/custom.less';
import '../less/public.less';
import ChartsIntro from './ChartsIntro';

const RightColumnLayout = (props) => {
  const { bodyContent, bodyFooter, bodyHeader, header, sideContent } = props;
  return (
    <div id="search-app">
      TEST LAYOUT
      <Grid columns={1} stackable className="body-content">
        <Grid.Row>
          <Grid.Column
            widescreen="12"
            tablet="12"
            computer="12"
            className="col-left"
          >
            <div>{bodyContent}</div>
          </Grid.Column>
        </Grid.Row>
      </Grid>
      <Grid className="body-footer">
        <Grid.Row>
          <Grid.Column widescreen={12}>{bodyFooter}</Grid.Column>
        </Grid.Row>
      </Grid>
    </div>
  );
};

export default RightColumnLayout;
