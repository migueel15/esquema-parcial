import { inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { OAuthService } from 'angular-oauth2-oidc';
import { authConfig } from './auth.config';
import { UserService } from './user.service';

@Injectable({
  providedIn: 'root',
})
export class AuthGoogleService {
  private oAuthService = inject(OAuthService);
  private router = inject(Router);
  private userService = inject(UserService);
  profile = signal<any>(null);

  constructor() {
    this.initConfiguration();
  }

  initConfiguration() {
    this.oAuthService.configure(authConfig);
    this.oAuthService.setupAutomaticSilentRefresh();
    this.oAuthService.loadDiscoveryDocumentAndTryLogin().then(() => {
      if (this.oAuthService.hasValidIdToken()) {
        const profile = this.oAuthService.getIdentityClaims();
        this.profile.set(profile);
        this.userService.setUserProfile(profile);
        console.log(this.userService.getUserProfile());
      } else {
        this.router.navigate(['/login']);
      }
    });
  }

  login() {
    this.oAuthService.initCodeFlow();
  }

  logout() {
    this.oAuthService.revokeTokenAndLogout();
    this.oAuthService.logOut();
    this.profile.set(null);
    this.userService.clearUserProfile();
  }

  getToken() {
    return this.oAuthService.getAccessToken();
  }

  getProfile() {
    return this.profile;
  }

  isAuthenticated() {
    return this.oAuthService.hasValidAccessToken();
  }
}