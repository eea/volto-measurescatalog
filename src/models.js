import { ResultModel } from '@eeacms/search';

export class ResultModelExtended extends ResultModel {
  get originOfMeasure() {
    return this._result['Origin of the measure']?.raw;
  }

  get descriptors() {
    return this._result['Descriptors']?.raw;
  }

  get sector() {
    return this._result['Sector']?.raw;
  }

  getVal = (field) => {
    const fields = {
      'Origin of the measure': this.originOfMeasure,
      Descriptors: this.descriptors,
      Sector: this.sector,
    };

    return fields[field];
  };
}
