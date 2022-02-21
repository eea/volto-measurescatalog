export const encodeFilters = (filters) => {
  // Input: array of filters [[name, value, type], [name, value, type], ...]
  // Output: uncoded URI params as used in search
  let res = '?size=n_10_n';
  let index = 0;
  for (let filter of filters) {
    res +=
      '&' +
      encodeURIComponent(`filters[${index}][field]`) +
      '=' +
      encodeURIComponent(filter[0]) +
      '&' +
      encodeURIComponent(`filters[${index}][values][0]`) +
      '=' +
      encodeURIComponent(filter[1]) +
      '&' +
      encodeURIComponent(`filters[${index}][type]`) +
      '=' +
      filter[2];

    index++;
  }

  return res;
};
