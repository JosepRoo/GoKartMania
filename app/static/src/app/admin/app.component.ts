import { MediaMatcher } from '@angular/cdk/layout';
import { ChangeDetectorRef, Component, OnDestroy } from '@angular/core';
import { MatIconRegistry, MatDialog } from '@angular/material';
import { LogoutDialogComponent } from './logout-dialog/logout-dialog.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AdminComponent implements OnDestroy {
  mobileQuery: MediaQueryList;
  showFiller: Boolean = false;

  private _mobileQueryListener: () => void;

  logOutDialogRef;
  user;
  isSuperAdmin;

  constructor(
    changeDetectorRef: ChangeDetectorRef,
    media: MediaMatcher,
    private matIconRegistry: MatIconRegistry,
    private dialog: MatDialog
  ) {
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    this.mobileQuery.addListener(this._mobileQueryListener);
    this.matIconRegistry.registerFontClassAlias('fontawesome', 'fa');
    this.user = localStorage.getItem('user');
    this.isSuperAdmin = localStorage.getItem('is_super_admin');
  }

  ngOnDestroy(): void {
    this.mobileQuery.removeListener(this._mobileQueryListener);
    if(this.logOutDialogRef){
      this.logOutDialogRef.close();
    }
  }

  openLogoutDialog(){
    this.logOutDialogRef = this.dialog.open(LogoutDialogComponent, {
      width: '70%',
    });
  }
  // tslint:disable-next-line:member-ordering
  shouldRun = [/(^|\.)plnkr\.co$/, /(^|\.)stackblitz\.io$/].some(h =>
    h.test(window.location.host)
  );
}
