% include("header.tpl", viewer=viewer) 

	<div class="container text-center">

	<div class="page-header">
		<h3>Better Search</h3>
	</div>

		<div class="row">

			<!-- (bootstrap magic) -->
			<div class="hidden-xs col-md-4 col-lg-4"></div>

			<!-- Form -->
			<div class="col-xs-12 col-md-4 col-lg-4">
				<form action="/search" method="post">
					<input class="d-none" name="searchtype" value="specific"/>

					<!-- Track title-->
					<div class="input-group">
						<!-- Icon -->
						<div class="input-group-prepend">
							<span class="input-group-text">
								<ion-icon name="musical-note"></ion-icon>
							</span>
						</div>
						<!-- Input -->
						<input class="form-control" placeholder="Track title" name="track" type="text" />
					</div>

					<!-- Artist -->
					<div class="input-group">
						<!-- Icon -->
						<div class="input-group-prepend">
							<span class="input-group-text">
								<ion-icon name="person"></ion-icon>
							</span>
						</div>
						<!-- Input -->
						<input class="form-control" placeholder="Artist" name="artist" type="text" />
					</div>

					<!-- Album -->
					<div class="input-group">
						<!-- Icon -->
						<div class="input-group-prepend">
							<span class="input-group-text">
								<ion-icon name="disc"></ion-icon>
							</span>
						</div>
						<!-- Input -->
						<input class="form-control" placeholder="Album" name="album" type="text" />
					</div>

					<br>

					<!-- Search button -->
					<div align="center input-group">
						<button class="btn btn-default" type="submit">
							Search  <ion-icon name="search" class="align-middle"></ion-icon>
						</button>
					</div>
				</form>

			</div>

			<!-- (bootstrap magic) -->
			<div class="hidden-xs col-md-4 col-lg-4"></div>

		</div> <!-- row -->
	</div> <!-- container -->

% include("footer.tpl", viewer=viewer)
