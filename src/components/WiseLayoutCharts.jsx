import React from 'react';
import { Grid } from 'semantic-ui-react';
import '../less/public.less';

const RightColumnLayout = (props) => {
  const { bodyContent } = props;
  return (
    <div id="search-app">
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
    </div>
  );
};

export default RightColumnLayout;
