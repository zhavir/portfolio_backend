import { SSTConfig } from 'sst';
import { Site } from './stacks/Function';
import { IAM } from './stacks/IAM';

export default {
  config(_input) {
    return {
      name: 'portfolio-backend',
      region: 'us-east-1',
    };
  },
  stacks(app) {
    app.stack(Site).stack(IAM);
  },
} satisfies SSTConfig;
