package thealphaversion.app.safe_cide;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.CardView;
import android.view.View;
import android.widget.GridLayout;
import android.widget.Toast;


public class HomeActivity extends AppCompatActivity {

    GridLayout gridLayout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        gridLayout= findViewById(R.id.mainGrid);
        setSingleEvent(gridLayout);

    }

    // we are setting onClickListener for each element
    private void setSingleEvent(GridLayout gridLayout) {
        for(int i = 0; i<gridLayout.getChildCount();i++){
            CardView cardView=(CardView)gridLayout.getChildAt(i);
            final int finalI= i;
            cardView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Toast.makeText(HomeActivity.this,"Clicked at index "+ finalI,
                            Toast.LENGTH_SHORT).show();
                    if(finalI==0){
                        Intent intent=new Intent(HomeActivity.this, ActivitesActivity.class);
                        startActivity(intent);
                    }
                    else if(finalI==1){
                        Intent intent=new Intent(HomeActivity.this, HelplineActivity.class);
                        startActivity(intent);
                    }
                    else if(finalI==2){
                        Intent intent=new Intent(HomeActivity.this, OnGroundActivity.class);
                        startActivity(intent);
                    }
                    else if(finalI==3){
                        Intent intent=new Intent(HomeActivity.this, GuidedBreathingActivity.class);
                        startActivity(intent);
                    }
                    else if(finalI==4){
                        Intent intent=new Intent(HomeActivity.this, VolunteerActivity.class);
                        startActivity(intent);
                    }
                    else if(finalI==5){
                        Intent intent=new Intent(HomeActivity.this, ContactActivity.class);
                        startActivity(intent);
                    }
                }
            });
        }

    }
}
