import React from 'react';
import { Item } from 'semantic-ui-react';
import { useAppConfig, String, ResultHeader } from '@eeacms/search';

const DescriptorItem = (props) => {
  const { descriptor, facets } = props;
  const descriptors = facets.filter((f) => f.field === 'Descriptors');
  return (
    <>
      {descriptors[0].facetValues
        .filter((d) => d.value === descriptor)
        .map((d, i) => (
          <a
            key={i}
            href={d.url}
            className="simple-item-link"
            target="_blank"
            rel="noreferrer"
          >
            {d.name}
          </a>
        ))}
    </>
  );
};

// needed because of weird use of component from react-search-ui
const Inner = (props) => {
  const { result } = props;
  const { appConfig } = useAppConfig();
  const { listingViewParams, facets = [] } = appConfig;
  const getVal = (field) => {
    return result.getVal(field);
  };

  return (
    <Item>
      <Item.Content>
        <ResultHeader {...props} {...listingViewParams} appConfig={appConfig} />
        <Item.Extra>
          {listingViewParams?.extraFields?.map(({ field, label }, i) =>
            field === 'Descriptors' ? (
              <div className="simple-item-extra descriptor-item" key={i}>
                <span className="simple-item-label">{label}:</span>{' '}
                {typeof getVal(field) === 'string' ? (
                  <DescriptorItem facets={facets} descriptor={getVal(field)} />
                ) : Array.isArray(getVal(field)) ? (
                  getVal(field).map((item, i) => (
                    <span key={i} className="array-string-item">
                      {i > 0 && ', '}
                      <DescriptorItem
                        key={i}
                        facets={facets}
                        descriptor={item}
                      />
                    </span>
                  ))
                ) : (
                  <DescriptorItem facets={facets} descriptor={getVal(field)} />
                )}
              </div>
            ) : (
              <div className="simple-item-extra" key={i}>
                <span className="simple-item-label">{label}:</span>{' '}
                <String val={getVal(field)} />
              </div>
            ),
          )}
        </Item.Extra>
      </Item.Content>
    </Item>
  );
};

const ResultItem = (props) => {
  return <Inner {...props} />;
};

export default ResultItem;
