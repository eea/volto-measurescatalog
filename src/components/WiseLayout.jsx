import React from 'react';
import { Grid } from 'semantic-ui-react';
// import '../less/custom.less';
import '../less/public.less';

const RightColumnLayout = (props) => {
  const { bodyContent, bodyFooter, bodyHeader, header, sideContent } = props;
  return (
    <div id="search-app">
      <Grid className="body-header">
        <Grid.Row>
          <Grid.Column widescreen={12}>
            <div>{header}</div>
            <div>{bodyHeader}</div>
          </Grid.Column>
        </Grid.Row>
      </Grid>
      <Grid columns={2} stackable className="body-content">
        <Grid.Row>
          <Grid.Column
            widescreen="10"
            tablet="10"
            computer="10"
            className="col-left"
          >
            <div>{bodyContent}</div>
          </Grid.Column>
          <Grid.Column
            widescreen="2"
            tablet="2"
            computer="2"
            className="col-right"
          >
            <h3>Filter by</h3>
            <div>{sideContent}</div>
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
