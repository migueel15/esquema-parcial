import { AuthConfig } from 'angular-oauth2-oidc';
import {environment} from '../../environments/environment';

export const authConfig: AuthConfig = {
  issuer: 'https://accounts.google.com',
  strictDiscoveryDocumentValidation: false,
  showDebugInformation: true,
  clientId: environment.CLIENT_ID_PEDRO,
  redirectUri: window.location.origin + '/dashboard',
  scope: 'openid profile email',
};
