import React from 'react';
import { Grid } from 'semantic-ui-react';
// import '../less/custom.less';
import '../less/base.less';
import '../less/wise.less';

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
            widescreen="9"
            tablet="8"
            computer="9"
            className="col-left"
          >
            <div>{bodyContent}</div>
          </Grid.Column>
          <Grid.Column
            widescreen="3"
            tablet="4"
            computer="3"
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
