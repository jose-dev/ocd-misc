package com.ocado.de.osp.carrots;

import com.google.inject.AbstractModule;
import com.google.inject.Scopes;
import com.google.inject.util.Modules;
import com.ocado.de.osp.tools.authentication.GoogleCredentialProvider;
import com.ocado.de.osp.tools.authentication.GoogleServiceAccountCredentialProvider;
import com.ocado.de.osp.tools.authentication.ServiceAccount;
import com.ocado.de.osp.tools.googlecloud.GoogleCloudModule;

public class CarrotsModule extends AbstractModule {

    @Override
    protected void configure() {
        install(Modules.override(GoogleCloudModule.createWithAllDependencies("dev-atm-eu-storage"))
                .with(new AbstractModule() {
                    @Override
                    protected void configure() {
                        bind(ServiceAccount.class).toInstance(ServiceAccount
                                .of("deosp-b2b@prd-atm-eu-datamanager.iam.gserviceaccount.com")
                                .withP12Key("/authentication/google/deosp-b2b@prd-atm-eu-datamanager.iam.gserviceaccount.com.p12"));
                        bind(GoogleCredentialProvider.class).to(GoogleServiceAccountCredentialProvider.class).in(Scopes.SINGLETON);
                    }
                }));
        bind(EventSink.class).asEagerSingleton();
    }

}
